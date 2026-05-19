# 音声認識＆音声合成サーバ

VOSKを使った音声認識とvoicevox_coreを使った音声合成サーバを作成します。
このサーバーは、Flaskを使って実装しています。

## 準備
VOSKとVoicevox_coreの準備をします。

### VOSKのインストール
VOSKは、pipでインストール可能ですので、requirement_vosk.txtに記載したモジュールをインストールします。

```
 pip install -r requirement_vosk.txt
```

次に音声認識のモデルをダウンロードします。
https://alphacephei.com/vosk/models
にある日本語のモデル(vosk-model-ja-0.22)をダウンロードします。

ダウンロードした、vosk-model-ja-0.22.zip をこのディレクトリで解凍します。

Linux:
```
url --ssl-no-revoke -O https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip
unzip vosk-model-ja-0.22.zip
```

Windows:
```
url --ssl-no-revoke -O https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip
tar xzvf vosk-model-ja-0.22.zip
```

### Voicevox_coreのインストール
Voicevox_coreの公式サイト( https://github.com/VOICEVOX/voicevox_core/releases )から最新版のダウンローダをダウンロードします。

Linux： download-linux-x64
Windows： download-windows-x64.exe

https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.4/download-windows-x64.exe

https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.4/voicevox_core-0.16.4-cp310-abi3-win_amd64.whl

https://github.com/VOICEVOX/voicevox_core/releases/download/0.16.4/voicevox_core-windows-x64-0.16.4.zip

次にダウンローダを実行します。
実行後、カレントディレクトリに、voicevox_coreというディレクトリにモデルや辞書等がダウンロードされます。

次に、Pythonのモジュールをダウンロードします。
ダウンローダと同じ場所に、voicevox_core-0.16.3-cp310-abi3-XXXXX.whl（XXXはOSによって変わります）がありますので、これをダウンロードします。


ダウンロードしたファイルをpipでインストールします。
```
pip install voicevox_core-0.16.3-cp310-abi3-XXXXX.whl
```
2025/12/14現在では、最新版は0.16.3でした。実際に実行する場合には、ダウンロードしたバージョンに置き換えてください。

また、このサーバでは、voicevox_coreで生成されたWAVデータ、8kHzに変換しています。そのためのモジュールとして、soundfile と resampyを使用していますので、こちらもインストールします。

```
pip install soundfile
pip install resampy
pip install audioop-lts
```
以上でvoicevox_coreのインストールは完了です。

## サーバーの起動
サーバのプログラムは、server.pyです。
このディレクトリで、下記のコマンドを実行します。

```
python server.py
```

以上で、Webサーバーが起動します。デフォルト設定では、8000番ポートを使用する設定にしています。
