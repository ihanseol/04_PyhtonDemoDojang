using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Threading;
using TestStack.White;
using TestStack.White.Configuration;
using TestStack.White.Factory;
using TestStack.White.InputDevices;
using TestStack.White.UIItems;
using TestStack.White.UIItems.Finders;
using TestStack.White.UIItems.WindowItems;

class Program
{
    private static readonly string PROGRAM_PATH = @"C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE";
    private static bool ISAQTOPEN = false;
    private static readonly string DIRECTORY = @"d:\05_Send\";
    private static readonly double DELAY = 0.5;
    private static bool IS_BLOCK = true;
    private static string G_COMPANY = "산수개발(주)";
    private static string G_ADDRESS = "주소";

    [DllImport("user32.dll")]
    public static extern void BlockInput(bool block);

    static void EnterProjectInfo(Window window)
    {
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.ALT);
        window.Keyboard.Enter("e");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.ALT);
        Thread.Sleep(200);
        window.Keyboard.Enter("r");
    }

    static void OpenAQT(string filename)
    {
        if (!ISAQTOPEN)
        {
            Process.Start(PROGRAM_PATH);
            ISAQTOPEN = true;
            Thread.Sleep(TimeSpan.FromSeconds(DELAY));
        }

        var application = Application.Attach(PROGRAM_PATH);
        var window = application.GetWindows().First();
        
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        window.Keyboard.Enter("o");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        
        window.Keyboard.Enter("backspace");
        window.Keyboard.Enter(DIRECTORY + filename);
        Thread.Sleep(TimeSpan.FromSeconds(DELAY));
        window.Keyboard.Enter("enter");
        Thread.Sleep(TimeSpan.FromSeconds(DELAY));
    }

    static void CloseAQT()
    {
        var application = Application.Attach(PROGRAM_PATH);
        var window = application.GetWindows().First();
        
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        window.Keyboard.Enter("s");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        Thread.Sleep(TimeSpan.FromSeconds(DELAY));
        
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.ALT);
        window.Keyboard.Enter("f4");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.ALT);
        Thread.Sleep(TimeSpan.FromSeconds(DELAY));
    }

    static void MainJob(string well, string address, string company)
    {
        Thread.Sleep(200);
        
        var application = Application.Attach(PROGRAM_PATH);
        var window = application.GetWindows().First();
        
        EnterProjectInfo(window);
        
        Clipboard.SetText(company);
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        window.Keyboard.Enter("v");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        
        for (int i = 0; i < 3; i++)
        {
            window.Keyboard.Enter("tab");
        }
        
        Clipboard.SetText(address);
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        window.Keyboard.Enter("v");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        
        Clipboard.SetText(well);
        window.Keyboard.Enter("tab");
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        window.Keyboard.Enter("v");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        
        window.Keyboard.Enter("tab");
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        window.Keyboard.Enter("v");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        
        window.Keyboard.Enter("enter");
        
        window.Keyboard.HoldKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        window.Keyboard.Enter("s");
        window.Keyboard.LeaveKey(TestStack.White.WindowsAPI.KeyboardInput.SpecialKeys.CONTROL);
        
        Thread.Sleep(TimeSpan.FromSeconds(DELAY));
    }

    static void Main(string[] args)
    {
        var options = new List<string> { "SanSu", "DaeWoong", "WooKyung", "HanIL", "DongHae", "HyunYoon", "JunIL", "BuYeo", "TaeYang", "SamWon", "MainGeo" };
        var companies = new List<string> { "산수개발(주)", "대웅엔지니어링 주식회사", "(주) 우경엔지니어링", "주식회사 한일지하수", "(주)동해엔지니어링", "(주)현윤이앤씨", "(주) 전일", "부여지하수개발 주식회사", "(주)태양이엔지", "삼원개발(주)", "마인지오 주식회사" };

        Console.WriteLine("Please choose your Company: ");
        for (int i = 0; i < options.Count; i++)
        {
            Console.WriteLine($"{i + 1}. {options[i]}");
        }

        int index = int.Parse(Console.ReadLine()) - 1;
        Console.WriteLine($"{options[index]} {index} {companies[index]}");

        Console.WriteLine("Enter the Company Address :");
        var address = Console.ReadLine();
        G_ADDRESS = string.IsNullOrWhiteSpace(address) ? "Empty Address" : address;

        if (IS_BLOCK)
        {
            BlockInput(true);
        }

        var files = Directory.GetFiles(DIRECTORY, "*.aqt");
        if (files.Length > 0)
        {
            for (int i = 1; i <= 32; i++) // maximum well number is 18
            {
                var wellFiles = files.Where(f => Path.GetFileName(f).StartsWith($"w{i}_")).ToList();
                if (wellFiles.Any())
                {
                    foreach (var file in wellFiles)
                    {
                        OpenAQT(Path.GetFileName(file));
                        MainJob($"W-{i}", G_ADDRESS, companies[index]);
                    }
                }
            }
            CloseAQT();
        }
        else
        {
            Console.WriteLine("AQT files not found...");
        }

        Thread.Sleep(500);

        if (IS_BLOCK)
        {
            BlockInput(false);
        }
    }
}
