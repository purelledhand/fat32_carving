from django.shortcuts import render
from .models import Carving
import os, sys
import struct

# Create your views here.

def parsing(request):
	bytes_per_sector = Carving.objects
	return render(request, 'parsing.html', {'Bytes_per_Sec': Bytes_per_Sec, 'Sec_per_Clust': Sec_per_Clust, 'cluster_size': cluster_size, 'reserve': Reserve, 'fat32_size': FAT32_size, 'fat1': FAT1, 'fat2': FAT2, 'rootdirectory': Root_Directory, 'num': num, 'cluster': rd_offset, 'type':file_type})

drive = open("\\\\.\\D:","rb")
drive.seek(0)
br = drive.read(512) # Boot Record

"""
*FAT 32 Structure*
MBR + Boot Record(128) + Reserved_area + FAT#1 + FAT#2 + Root Directory + Data

*Boot Record*
jump boot code + OEM + bytes per sector(11~12) + sectors per cluster(13) + reserved sector count(14~15)
... + fat 32 size (36~39) + ...

"""

# BR에서 offset 구하기

if "MSDOS" in str(br[:0x10]):

    Bytes_per_Sec = struct.unpack_from("<H", br[0x0B:0x0D])[0] # 4byte
    Sec_per_Clust = struct.unpack_from("<b", br[0x0D:0x0E])[0] # 2byte
    cluster_size = Sec_per_Clust * Bytes_per_Sec

    Reserve = struct.unpack_from("<H", br[0x0E:0x10])[0] # 4byte
    FAT32_size = struct.unpack_from("<H", br[0x24:0x27])[0] # 8byte

    FAT1 = Reserve # FAT#1 = Reserved area + Boot Recorder // boot recorder 크기를 더하면 drive 크기를 초과해버림..
    FAT2 = FAT1 + FAT32_size
    Root_Directory = FAT2 + FAT32_size

    #print(Bytes_per_Sec)
    #print(Sec_per_Clust)
    #print(cluster_size)
    #print(br[0x1FE:].hex())

# file signature를 list에 저장

    filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/signature_list.txt')

    f = open(filepath, 'r')
    signature = []
    lines = f.readlines()
    for i in lines:
        signature.append(i)
    f.close()

# root directory에서 file info 확인 (root directory에서 파일 한개당 32byte씩이니까 32byte씩 읽어오기)
    num = 0
    for i in range(0, int(FAT32_size/4)):
        rd_file = (i * 32)
        rd_offset = Root_Directory + rd_file
        drive.seek(rd_offset)
        file = drive.read(32).hex()
        #print(file[:16])

        for sig in signature:
            file_signature = sig[6:].strip()
            file_type = sig[:4].strip()
            if file_signature in file:
                #ftype = file_type // 이렇게 하면 ftype이 초기화 되지 않아서 서버가 돌아가지 않음. root directory에 해당하는 파일 시그니처가 없다는 의미..
                num = num + 1
                break;

        break;        

else :
    print("This Filesystem is not FAT32.")
    print("FileSystem INFO : "+str(br[:16]))