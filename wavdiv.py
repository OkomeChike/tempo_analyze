import wave
import struct
import math
import os
from scipy import fromstring, int16

# すでに同じ名前のディレクトリが無いか確認
file = os.path.exists("output")
print(file)

if file == False:
    #保存先ディレクトリの作成
    os.mkdir("output")

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
    print("channel : ", ch)
    print("sample width : ", width)
    print("frame rate : ", fr)
    print("frame num : ", fn)
    print("params : ", wr.getparams())
    print("total time : ", total_time)
    print("total time(integer) : ", integer)
    print("time : ", t)
    print("frames : ", frames)
    print("number of cut : ", num_cut)

    # waveの実データを取得し数値化
    data = wr.readframes(wr.getnframes())
    wr.close()
    X = fromstring(data, dtype=int16)
    print(X)

    for i in range(num_cut):
        print(i)
        #出力データを生成
        outf = 'output/' + str(i) + '.wav' 
        start_cut = i*frames
        end_cut = i*frames + frames
        print(start_cut)
        print(end_cut)
        Y = X[start_cut:end_cut]
        outd = struct.pack("h" * len(Y), *Y)

        # 書き出し
        ww = wave.open(outf, 'w')
        ww.setnchannels(ch)
        ww.setsampwidth(width)
        ww.setframerate(fr)
        ww.writeframes(outd)
        ww.close()


f_name = input('input filename -> ')
cut_time = input('input cut time -> ')
cut_wav(f_name,cut_time)
