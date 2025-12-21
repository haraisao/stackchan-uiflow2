# 音声認識＆音声合成サーバ

VOSKを使った音声認識とvoicevox_coreを使った音声合成サーバを作成します。
このサーバーは、Falskを使って実装しています。

## 準備
VOSKとVoicevox_coreの準備をします。

### VOSKのインストール
VOSKは、pipでインストール可能ですので、requiremet_vosk.txtに記載したモジュールをインストールします。

```
 pip install -r requirement_vosk.txt
```

次に音声認識のモデルをダウンロードします。
https://alphacephei.com/vosk/models
にある日本語のモデル(vosk-model-ja-0.22)をダインロードします。

ダウンロードした、vosk-model-ja-0.22.zip をこのディレクトリで回答します。

Linux:
```
unzip vosk-model-ja-0.22
```

Windows:
```
tar xzvf vosk-model-ja-0.22.zip
```

### Voicevox_coreのインストール
Voicevox_coreの公式サイト( https://github.com/VOICEVOX/voicevox_core/releases )から最新版のダウンローダをダウンロードします。

Linux： download-linux-x64
Window： download-windows-x64.exe

次にダウンローダを実行します。
実行後、カレントディレクトリに、voicevox_coreというディレクトリにモデルや辞書等がダウンロードされます。

次に、Pythonのモジュールをダウンロードします。
ダウンローダと同じ場所に、voicevox_core-0.16.3-cp310-abi3-XXXXX.whl（XXXはOSによって変わります）がありますので、これをダウンロードします。

ダウンロードしたファイルをpipでインストールします。
```
pip install voicevox_core-0.16.3-cp310-abi3-XXXXX.whl
```

また、このサーバでは、voicevox_coreで生成されたWAVデータ、8kHzに変換しています。そのためのモジュールとして、soundfile と resampyを使用していますので、こちらもインストールします。

```
pip install soundfile
pip install resampy
```
以上でvoicevox_coreのインストールは完了です。

## サーバーの起動
サーバのプログラムは、server.pyです。
このディレクトリで、下記のコマンドを実行します。

```
python server.py
```

以上で、Webサーバーが起動します。デフォルト設定では、8000番ポートを使用する設定にしています。
