unit KakaoLocalAPI;

interface

uses
  System.SysUtils, System.Classes, System.JSON, System.Variants,
  System.Net.HttpClient, System.Net.URLClient, Vcl.Clipbrd;

type
  TKakaoLocalAPI = class
  private
    FREST_API_KEY: string;
    FHttpClient: THTTPClient;
    
    function ExtractCoordinates(const JsonData: TJSONArray): TPair<string, string>;
    procedure TransformCoordinates(const X, Y: string);
  public
    constructor Create(const API_KEY: string);
    destructor Destroy; override;
    
    procedure SearchAddress(const Address: string);
  end;

implementation

{ TKakaoLocalAPI }

constructor TKakaoLocalAPI.Create(const API_KEY: string);
begin
  inherited Create;
  FREST_API_KEY := API_KEY;
  FHttpClient := THTTPClient.Create;
  FHttpClient.CustomHeaders['Authorization'] := Format('KakaoAK %s', [FREST_API_KEY]);
end;

destructor TKakaoLocalAPI.Destroy;
begin
  FHttpClient.Free;
  inherited;
end;

function TKakaoLocalAPI.ExtractCoordinates(const JsonData: TJSONArray): TPair<string, string>;
var
  FirstItem: TJSONObject;
begin
  Result := TPair<string, string>.Create('', '');
  
  if (JsonData = nil) or (JsonData.Count = 0) then
    Exit;
    
  FirstItem := JsonData.Items[0] as TJSONObject;
  Result.Key := FirstItem.GetValue<string>('x');
  Result.Value := FirstItem.GetValue<string>('y');
end;

procedure TKakaoLocalAPI.TransformCoordinates(const X, Y: string);
var
  URL: string;
  Response: IHTTPResponse;
  JsonData: TJSONObject;
  Documents: TJSONArray;
  TransformedX, TransformedY: string;
  CoordinateText: string;
begin
  URL := Format('https://dapi.kakao.com/v2/local/geo/transcoord.json?x=%s&y=%s&input_coord=WGS84&output_coord=TM', [X, Y]);
  Response := FHttpClient.Get(URL);
  
  if Response.StatusCode = 200 then
  begin
    JsonData := TJSONObject.ParseJSONValue(Response.ContentAsString) as TJSONObject;
    try
      Documents := JsonData.GetValue<TJSONArray>('documents');
      if (Documents <> nil) and (Documents.Count > 0) then
      begin
        TransformedX := (Documents.Items[0] as TJSONObject).GetValue<string>('x');
        TransformedY := (Documents.Items[0] as TJSONObject).GetValue<string>('y');
        
        WriteLn(Format('x: %s', [TransformedX]));
        WriteLn(Format('y: %s', [TransformedY]));
        WriteLn('----------------------------------------------------------------------------------------------------');
        
        CoordinateText := Format('%s,%s', [TransformedX, TransformedY]);
        Clipboard.AsText := CoordinateText;
        WriteLn(CoordinateText);
      end;
    finally
      JsonData.Free;
    end;
  end;
end;

procedure TKakaoLocalAPI.SearchAddress(const Address: string);
var
  URL: string;
  Response: IHTTPResponse;
  JsonData: TJSONObject;
  Documents: TJSONArray;
  AddressData: string;
  Coordinates: TPair<string, string>;
begin
  URL := 'https://dapi.kakao.com/v2/local/search/address.json';
  
  WriteLn('----------------------------------------------------------------------------------------------------');
  
  Response := FHttpClient.Get(URL + '?query=' + TNetEncoding.URL.Encode(Address));
  
  if Response.StatusCode = 200 then
  begin
    JsonData := TJSONObject.ParseJSONValue(Response.ContentAsString) as TJSONObject;
    try
      Documents := JsonData.GetValue<TJSONArray>('documents');
      WriteLn(Format('documents: %s', [Documents.ToJSON]));
      
      AddressData := '';
      
      if (Documents <> nil) and (Documents.Count > 0) then
      begin
        AddressData := ((Documents.Items[0] as TJSONObject).GetValue<TJSONObject>('address')).GetValue<string>('address_name');
      end;
      
      WriteLn('----------------------------------------------------------------------------------------------------');
      WriteLn(AddressData);
      WriteLn('----------------------------------------------------------------------------------------------------');
      
      Coordinates := ExtractCoordinates(Documents);
      WriteLn(Format('x: %s, y: %s', [Coordinates.Key, Coordinates.Value]));
      WriteLn('----------------------------------------------------------------------------------------------------');
      
      if (Coordinates.Key <> '') and (Coordinates.Value <> '') then
        TransformCoordinates(Coordinates.Key, Coordinates.Value);
        
      WriteLn('----------------------------------------------------------------------------------------------------');
      Write('종료하시려면 엔터키를 누르세요 ~ ');
      ReadLn;
    finally
      JsonData.Free;
    end;
  end;
end;

end.
