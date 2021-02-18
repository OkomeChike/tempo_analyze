import numpy as np
import librosa
import wave
import struct
import math
import os
from scipy import fromstring, int16
import matplotlib.pyplot as plt 

#----------------------------------------
# wavファイルの分割
#---------------------------------------

def cut_wav(filename, time):
    #ファイル読み出し
    wavf = filename + '.wav'
    wr = wave.open(wavf, 'r')

    #waveファイルが持つ性質を取得
    ch = wr.getnchannels()
    width = wr.getsampwidth()
    fr = wr.getframerate()
    fn = wr.getnframes()
    total_time = 1.0 * fn / fr
    integer = math.floor(total_time)
    t = int(time)
    frames = int(ch * fr * t)
    num_cut = int(integer//t)

    # 確認用
    print("total time(s) : ", total_time)
    print("total time(integer) : ", integer)
    print("time : ", t)
    print("number of cut : ", num_cut)

    # waveの実データを取得し数値化
    data = wr.readframes(wr.getnframes())
    wr.close()
    X = np.frombuffer(data, dtype=int16)

    print()

    for i in range(num_cut):
        print(str(i) + ".wav --> OK!")
        #出力データを生成
        outf = 'output/' + str(i) + '.wav' 
        start_cut = i*frames
        end_cut = i*frames + frames
        Y = X[start_cut:end_cut]
        outd = struct.pack("h" * len(Y), *Y)

        # 書き出し
        ww = wave.open(outf, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(outd)
        ww.close()
    return num_cut

#----------------------------------------
# 全体のテンポを求める
#---------------------------------------
def totaltempo(filename):
    #検索するファイル名の作成 => output/ i .wav
    name = filename + ".wav"

    #wavファイルの読み込み
    y, sr = librosa.load(name)

    #テンポとビートの抽出
    tempo , beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    #全体のテンポを表示
    print()
    print("total tempo : ", int(tempo))
    print()

#----------------------------------------
# 分割テンポを求める
#---------------------------------------

def temposearch(num, time):
    #return用変数の宣言
    l = []
    t = []
    t_time = 0
    before_tempo = 0

    print("division tempo")

    #音楽の読み込み
    for i in range(0,num,1):
        #検索するファイル名の作成 => output/ i .wav
        name = "output/" + str(i) + ".wav"

        #wavファイルの読み込み
        y, sr = librosa.load(name)

        #テンポとビートの抽出
        tempo , beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        int_tempo = int(tempo)

        #テンポの表示
        print(str(i+1) +  ":" + str(int_tempo))

        #return用変数へ代入
        l.append(int_tempo)
        t_time = t_time + int(time)
        t.append(t_time)
    
    return l, t



#---------------------------------
# メイン関数
#---------------------------------
if __name__ == '__main__':
    # すでに同じ名前のディレクトリが無いか確認
    file = os.path.exists("output")
    print(file)

    if file == False:
        #保存先ディレクトリの作成
        os.mkdir("output")

    #ファイル名とカット時間を入力しwavファイルを分割
    f_name = input('input filename -> ')
    cut_time = input('input cut time -> ')
    n = int(cut_wav(f_name,cut_time))

    #テンポ解析
    totaltempo(f_name)
    tempo, time = temposearch(n, cut_time)

    print()

    #タイトル用
    name = "テンポ解析 " + cut_time + "秒で分割"

    #グラフ描写
    plt.title(name, fontname="MS Gothic")
    plt.xlabel("時間(s)", fontname="MS Gothic")
    plt.ylabel("テンポ(bpm)", fontname="MS Gothic")
    plt.ylim(60, 180)
    plt.plot(time, tempo)
    plt.show()


