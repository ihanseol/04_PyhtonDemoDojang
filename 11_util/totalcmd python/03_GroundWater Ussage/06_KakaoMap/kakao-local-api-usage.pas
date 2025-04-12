program KakaoLocalAPIDemo;

{$APPTYPE CONSOLE}

uses
  System.SysUtils,
  KakaoLocalAPI in 'KakaoLocalAPI.pas';

var
  KakaoAPI: TKakaoLocalAPI;
begin
  try
    KakaoAPI := TKakaoLocalAPI.Create('bb159a41d2eb8d5acb71e0ef1dde4d16');
    try
      KakaoAPI.SearchAddress('충청남도 예산군 대술면 화산리 607-1');
    finally
      KakaoAPI.Free;
    end;
  except
    on E: Exception do
      WriteLn('Error: ', E.Message);
  end;
  
  Write('Press Enter to exit...');
  ReadLn;
end.
