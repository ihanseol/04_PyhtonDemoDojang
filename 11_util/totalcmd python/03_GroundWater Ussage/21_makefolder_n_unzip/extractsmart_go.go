package main

import (
	"archive/tar"
	"archive/zip"
	"bufio"
	"compress/gzip"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"sort"
	"strings"
	"syscall"

	"github.com/mholt/archiver/v4"
	"github.com/nwaples/rardecode/v2"
)

// ArchiveContents represents the contents of an archive
type ArchiveContents struct {
	Files   []string
	Folders []string
}

// ExtractSmart handles archive extraction and analysis
type ExtractSmart struct {
	SendPath   string
	WinRarPath string
}

// NewExtractSmart creates a new ExtractSmart instance
func NewExtractSmart(sendPath, winrarPath string) *ExtractSmart {
	if sendPath == "" {
		sendPath = "d:\\05_Send\\"
	}
	if winrarPath == "" {
		winrarPath = `C:\Program Files\WinRAR\WinRar.exe`
	}
	
	return &ExtractSmart{
		SendPath:   sendPath,
		WinRarPath: winrarPath,
	}
}

// PrintDebug prints debug message with decorative characters
func (es *ExtractSmart) PrintDebug(msg, chr string, length int) {
	if chr == "" {
		chr = "*"
	}
	if length == 0 {
		length = 180
	}
	
	fmt.Println(strings.Repeat(chr, length))
	fmt.Println(msg)
	fmt.Println(strings.Repeat(chr, length))
}

// ShowMessageBox displays a message box (Windows only)
func (es *ExtractSmart) ShowMessageBox(message string) error {
	// For Windows, we can use syscall to show message box
	if isWindows() {
		return showWindowsMessageBox(message)
	}
	
	// For other platforms, just print to console
	fmt.Printf("Notice: %s\n", message)
	return nil
}

// isWindows checks if running on Windows
func isWindows() bool {
	return os.PathSeparator == '\\'
}

// showWindowsMessageBox shows a Windows message box
func showWindowsMessageBox(message string) error {
	user32 := syscall.NewLazyDLL("user32.dll")
	messageBoxW := user32.NewProc("MessageBoxW")
	
	title, _ := syscall.UTF16PtrFromString("Notice")
	text, _ := syscall.UTF16PtrFromString(message)
	
	messageBoxW.Call(
		uintptr(0),
		uintptr(unsafe.Pointer(text)),
		uintptr(unsafe.Pointer(title)),
		uintptr(0),
	)
	
	return nil
}

// CopyFile copies a file from source to target
func (es *ExtractSmart) CopyFile(sourceFile, targetFile string) error {
	source, err := os.Open(sourceFile)
	if err != nil {
		fmt.Printf("Source file not found: %s\n", sourceFile)
		return err
	}
	defer source.Close()

	target, err := os.Create(targetFile)
	if err != nil {
		fmt.Printf("Permission denied. Could not copy to %s\n", targetFile)
		return err
	}
	defer target.Close()

	_, err = io.Copy(target, source)
	if err != nil {
		fmt.Printf("An error occurred: %v\n", err)
		return err
	}

	fmt.Printf("File copied successfully from %s to %s\n", sourceFile, targetFile)
	return nil
}

// GetArchiveContents returns the top-level files and folders in an archive
func (es *ExtractSmart) GetArchiveContents(archivePath string) (*ArchiveContents, error) {
	if _, err := os.Stat(archivePath); os.IsNotExist(err) {
		return nil, fmt.Errorf("파일을 찾을 수 없습니다: %s", archivePath)
	}

	extension := strings.ToLower(filepath.Ext(archivePath))

	switch extension {
	case ".zip":
		return es.getZipContents(archivePath)
	case ".tar", ".gz", ".tgz":
		return es.getTarContents(archivePath)
	case ".rar":
		return es.getRarContents(archivePath)
	case ".7z":
		return es.get7zContents(archivePath)
	default:
		return nil, fmt.Errorf("지원하지 않는 압축 형식입니다: %s", extension)
	}
}

// getZipContents gets contents of ZIP file
func (es *ExtractSmart) getZipContents(zipPath string) (*ArchiveContents, error) {
	var files []string
	folders := make(map[string]bool)

	reader, err := zip.OpenReader(zipPath)
	if err != nil {
		return nil, err
	}
	defer reader.Close()

	for _, file := range reader.File {
		pathParts := strings.Split(file.Name, "/")
		
		if len(pathParts) == 1 && !strings.HasSuffix(file.Name, "/") {
			// Top-level file
			files = append(files, file.Name)
		} else if len(pathParts) >= 1 {
			// Top-level folder
			topFolder := pathParts[0]
			if topFolder != "" {
				folders[topFolder] = true
			}
		}
	}

	folderList := make([]string, 0, len(folders))
	for folder := range folders {
		folderList = append(folderList, folder)
	}
	sort.Strings(folderList)

	return &ArchiveContents{
		Files:   files,
		Folders: folderList,
	}, nil
}

// getTarContents gets contents of TAR file
func (es *ExtractSmart) getTarContents(tarPath string) (*ArchiveContents, error) {
	var files []string
	folders := make(map[string]bool)

	file, err := os.Open(tarPath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var reader io.Reader = file
	
	// Handle compressed tar files
	if strings.HasSuffix(tarPath, ".gz") || strings.HasSuffix(tarPath, ".tgz") {
		gzReader, err := gzip.NewReader(file)
		if err != nil {
			return nil, err
		}
		defer gzReader.Close()
		reader = gzReader
	}

	tarReader := tar.NewReader(reader)

	for {
		header, err := tarReader.Next()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}

		pathParts := strings.Split(header.Name, "/")
		
		if len(pathParts) == 1 && header.Typeflag == tar.TypeReg {
			// Top-level file
			files = append(files, header.Name)
		} else if len(pathParts) >= 1 {
			// Top-level folder
			topFolder := pathParts[0]
			if topFolder != "" {
				folders[topFolder] = true
			}
		}
	}

	folderList := make([]string, 0, len(folders))
	for folder := range folders {
		folderList = append(folderList, folder)
	}
	sort.Strings(folderList)

	return &ArchiveContents{
		Files:   files,
		Folders: folderList,
	}, nil
}

// getRarContents gets contents of RAR file
func (es *ExtractSmart) getRarContents(rarPath string) (*ArchiveContents, error) {
	var files []string
	folders := make(map[string]bool)

	file, err := os.Open(rarPath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader, err := rardecode.NewReader(file, "")
	if err != nil {
		return nil, err
	}

	for {
		header, err := reader.Next()
		if err == io.EOF {
			break
		}
		if err != nil {
			return nil, err
		}

		pathParts := strings.Split(header.Name, "/")
		
		if len(pathParts) == 1 && !header.IsDir {
			// Top-level file
			files = append(files, header.Name)
		} else if len(pathParts) >= 1 {
			// Top-level folder
			topFolder := pathParts[0]
			if topFolder != "" {
				folders[topFolder] = true
			}
		}
	}

	folderList := make([]string, 0, len(folders))
	for folder := range folders {
		folderList = append(folderList, folder)
	}
	sort.Strings(folderList)

	return &ArchiveContents{
		Files:   files,
		Folders: folderList,
	}, nil
}

// get7zContents gets contents of 7z file
func (es *ExtractSmart) get7zContents(sevenzPath string) (*ArchiveContents, error) {
	// For 7z, we'll use the archiver library or system command
	// This is a simplified implementation
	var files []string
	folders := make(map[string]bool)

	// Using archiver library for 7z support
	format, reader, err := archiver.Identify("", sevenzPath)
	if err != nil {
		return nil, err
	}

	if ex, ok := format.(archiver.Extractor); ok {
		file, err := os.Open(sevenzPath)
		if err != nil {
			return nil, err
		}
		defer file.Close()

		err = ex.Extract(reader, nil, func(ctx archiver.FileInfo) error {
			pathParts := strings.Split(ctx.NameInArchive, "/")
			
			if len(pathParts) == 1 && !ctx.IsDir() {
				// Top-level file
				files = append(files, ctx.NameInArchive)
			} else if len(pathParts) >= 1 {
				// Top-level folder
				topFolder := pathParts[0]
				if topFolder != "" {
					folders[topFolder] = true
				}
			}
			return nil
		})
		
		if err != nil {
			return nil, err
		}
	}

	folderList := make([]string, 0, len(folders))
	for folder := range folders {
		folderList = append(folderList, folder)
	}
	sort.Strings(folderList)

	return &ArchiveContents{
		Files:   files,
		Folders: folderList,
	}, nil
}

// PrintArchiveContents prints archive contents nicely and returns total count
func (es *ExtractSmart) PrintArchiveContents(archivePath string) (int, error) {
	fmt.Printf("\n📁 압축파일: %s\n", archivePath)
	fmt.Println(strings.Repeat("=", 50))

	contents, err := es.GetArchiveContents(archivePath)
	if err != nil {
		fmt.Printf("압축파일 읽기 오류: %v\n", err)
		return 0, err
	}

	if len(contents.Folders) > 0 {
		fmt.Println("📂 폴더:")
		for _, folder := range contents.Folders {
			fmt.Printf("  └── %s/\n", folder)
		}
	}

	if len(contents.Files) > 0 {
		fmt.Println("📄 파일:")
		for _, file := range contents.Files {
			fmt.Printf("  └── %s\n", file)
		}
	}

	if len(contents.Folders) == 0 && len(contents.Files) == 0 {
		fmt.Println("빈 압축파일이거나 읽을 수 없습니다.")
	}

	totalCount := len(contents.Folders) + len(contents.Files)
	fmt.Printf("\n총 %d개 폴더, %d개 파일\n", len(contents.Folders), len(contents.Files))

	// Special case: single file at root level
	if totalCount == 1 && len(contents.Folders) == 0 {
		totalCount = 99
	}

	return totalCount, nil
}

// ExtractArchive extracts archive to target directory
func (es *ExtractSmart) ExtractArchive(archivePath, targetDir string) error {
	// Analyze archive contents
	numFiles, err := es.PrintArchiveContents(archivePath)
	if err != nil {
		return err
	}
	
	isSingleFolder := (numFiles == 1)

	// Build WinRAR extraction command
	var extractCommand []string
	if isSingleFolder {
		extractCommand = []string{es.WinRarPath, "x", "-Y", archivePath, targetDir}
	} else {
		extractCommand = []string{es.WinRarPath, "x", "-ad", "-Y", archivePath, targetDir}
	}

	// Execute extraction
	cmd := exec.Command(extractCommand[0], extractCommand[1:]...)
	err = cmd.Run()
	if err != nil {
		fmt.Printf("압축 해제 중 오류 발생: %v\n", err)
		return err
	}

	fmt.Println("압축 해제가 완료되었습니다.")
	return nil
}

// ProcessArchiveList processes archives from a list file
func (es *ExtractSmart) ProcessArchiveList(listFilePath, targetDir string) error {
	err := os.Chdir(targetDir)
	if err != nil {
		return err
	}
	
	cwd, _ := os.Getwd()
	fmt.Printf("작업 디렉터리: %s\n", cwd)

	file, err := os.Open(listFilePath)
	if err != nil {
		es.ShowMessageBox(fmt.Sprintf("파일을 찾을 수 없습니다: %s", listFilePath))
		return fmt.Errorf("파일 목록 처리 중 오류 발생, %s: %v", listFilePath, err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		cleanPath := strings.ReplaceAll(strings.ReplaceAll(line, "\n", ""), "\\", "\\\\")
		fmt.Printf("처리 중: %s\n", cleanPath)

		err := es.ExtractArchive(cleanPath, targetDir)
		if err != nil {
			fmt.Printf("추출 실패: %v\n", err)
		}
	}

	return scanner.Err()
}

// RunMainProcess runs the main extraction process
func (es *ExtractSmart) RunMainProcess() {
	args := os.Args
	fmt.Printf("인수 개수: %d\n", len(args))
	fmt.Printf("스크립트 이름: %s\n", args[0])

	for i, arg := range args[1:] {
		fmt.Printf("인수 %d: %s\n", i+1, arg)
	}

	if len(args) < 3 {
		fmt.Println("사용법: extractsmart <source_file> <target_dir>")
		return
	}

	localAppData := os.Getenv("LOCALAPPDATA")
	sourceFile := filepath.Join(localAppData, "Temp", filepath.Base(args[1]))
	targetDir := args[2]

	// Copy file
	targetFile := filepath.Join(es.SendPath, "dir_list.txt")
	err := es.CopyFile(sourceFile, targetFile)
	if err != nil {
		fmt.Printf("파일 복사 실패: %v\n", err)
		return
	}
	
	sourceFile = targetFile

	fmt.Printf("1. 원본: %s\n", sourceFile)
	fmt.Printf("2. 대상: %s\n", targetDir)

	// Process archive list
	err = es.ProcessArchiveList(sourceFile, targetDir)
	if err != nil {
		fmt.Printf("압축파일 목록 처리 실패: %v\n", err)
	}

	// Remove temporary file
	err = os.Remove(sourceFile)
	if err != nil {
		fmt.Printf("임시 파일 삭제 실패: %v\n", err)
	} else {
		fmt.Printf("임시 파일 삭제됨: %s\n", sourceFile)
	}
}

func main() {
	// Create ExtractSmart instance
	extractor := NewExtractSmart("", "")

	// If command line arguments exist, run main process
	if len(os.Args) > 1 {
		extractor.RunMainProcess()
	} else {
		// Test mode
		fmt.Println("ExtractSmart 테스트 모드")

		// Example archive files
		testArchives := []string{
			"d:\\05_Send\\02_롯데부여리조트 - 전일.rar",
			"d:\\11_exaData\\06_util\\99_Game\\01_ToatalCommander Plugin\\00_Program Data\\25_Editor.rar",
		}

		for _, archiveFile := range testArchives {
			if _, err := os.Stat(archiveFile); err == nil {
				_, err := extractor.PrintArchiveContents(archiveFile)
				if err != nil {
					fmt.Printf("❌ %s: %v\n", archiveFile, err)
				}
			} else {
				fmt.Printf("⚠️ 파일이 존재하지 않습니다: %s\n", archiveFile)
			}
		}

		fmt.Println("\n클래스 기반 ExtractSmart가 준비되었습니다.")
		fmt.Println("사용법:")
		fmt.Println("1. 명령행에서: extractsmart <source_file> <target_dir>")
		fmt.Println("2. 코드에서: extractor := NewExtractSmart(\"\", \"\"); extractor.ExtractArchive(archivePath, targetDir)")
	}
}