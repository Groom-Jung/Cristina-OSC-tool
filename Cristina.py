'''
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import vxi11
import time
import PySimpleGUI as sg
import os
# 窗口内的所有控件.

layout = [  [sg.Text('示波器IP地址：'), sg.InputText('169.254.116.16',size=(40,1),enable_events=True, key='OSCIP')
				,sg.Text('运行状态：'), sg.Text(size=(5,1),enable_events=True, key='status',background_color='green')],
			[sg.Text('本机IP地址：'), sg.InputText('169.254.97.100',size=(40,1),enable_events=True, key='PCIP')
				,sg.Button('Connect'),sg.Text('未连接',key='TCONN',size=(8,1))],
			[sg.Text('保存路径(路径最后不带/)：'), sg.InputText(size=(40,1),enable_events=True, key='pathF')
				, sg.SaveAs('path', file_types=(('ALL Files', '*.PNG'),))],
			[sg.Text('文件名称(文件不带后缀)：'), sg.InputText(size=(40,1),enable_events=True, key='saveF')
				, sg.Button('save')],
			[sg.Text('设置label：')],
			[sg.Text('CH1:'),sg.InputText(size=(10,1)), sg.Text('CH2:'),sg.InputText(size=(10,1))
				,sg.Text('CH3:'),sg.InputText(size=(10,1)), sg.Text('CH4:'),sg.InputText(size=(10,1)), sg.Button('do',key='doL')],
			[sg.Text('设置采样格式：eg:10E-9代表10ns,10E6代表10M采样深度或10MS/s')],
			[sg.Text('SCALE:'),sg.InputText(size=(10,1))
				,sg.Text('LENGTH:'),sg.InputText(size=(10,1))
				,sg.Text('RATE:'), sg.InputText(size=(10,1)), sg.Button('do',key='doA')],
			[sg.Text('设置触发模式：')],
			[sg.Text('SOURCE:'),sg.InputCombo(('CH1','CH2','CH3','CH4'),size=(5,1)), sg.Text('EDGE:')
				, sg.InputCombo(('RISE','FALL','EITHER'), size=(5,1)), sg.Button('do',key='doT')], 
			[sg.Text('命令模式：'), sg.Text('CMD:'),sg.InputText(size=(30,1)), sg.Button('write'), sg.Button('read'), sg.Button('query')],
			[sg.Text('脚本模式：'), sg.Text('PATH:'),sg.InputText(size=(30,1)), sg.FileBrowse('open',key='pathS'), sg.Button('run')],
			[sg.Text('Meas Gating:'),sg.InputCombo(('off','screen','cursor'),size=(5,1),key='measGate'), sg.Button('do',key='doM')],
			[sg.Output(size=(70,10))]
			]

# 生成窗口
window = sg.Window('Tek示波器小助手', layout)
window.Finalize()
window.refresh()
print('Cristina Version 1.1 \r\nDate:2020-01-19\r\nMade by Groom')
print('Device List: MDO3k、MDO/MSO/DPO4k、DPO/MSO5k、DPO/DSA/DSO7k')
window.refresh()
# 消息处理和输入消息接收
OSCIP = ''
PCIP = ''
OSCPN = ''
ConnFlag = 0
	

def saveForTek3k():
    inst = vxi11.Instrument(OSCIP)
    inst.write(PCIP)
    inst.write('HARDCopy:ACTIVeprinter "labprn2"')
    inst.write('Hardcopy start')
    image = inst.read_raw()
    filePath = window.Element('pathF').get()
    fileName = window.Element('saveF').get()
    temp = filePath+'/'+fileName+".png"
    my_file = open( temp , "wb")
    my_file.write(image)
    my_file.close()
    inst.close()
    print(temp)
    if os.path.isfile(temp):
        print('saved successfully')
    else:
        print('saved failed')

def saveForTek5k():
    inst = vxi11.Instrument(OSCIP)
    inst.write('HARDCOPY:PORT FILE')
    inst.write('HARDCOPY:FILENAME "C:/Windows/temp"')
    inst.write('Hardcopy start')
    time.sleep(0.5)
    inst.write('filesystem:readfile "C:/Windows/temp.png"')
    image = inst.read_raw()
    filePath = window.Element('pathF').get()
    fileName = window.Element('saveF').get()
    temp = filePath+'/'+fileName+".png"
    my_file = open( temp , "wb")
    my_file.write(image)
    inst.write('FILESystem:DELEte "C:/Windows/temp.png"')	
    inst.close()
    print(temp)
    if os.path.isfile(temp):
        print('saved successfully')
    else:
        print('saved failed')
	
def setLabelForTek3k():
    inst = vxi11.Instrument(OSCIP)
    if CH1Name != '':
        temp = 'CH1:LABel '+'"'+CH1Name+'"'
        inst.write(temp)
        print(temp)
    if CH2Name != '':
        temp = 'CH2:LABel '+'"'+CH2Name+'"'
        inst.write(temp)
        print(temp)
    if CH3Name != '':
        temp = 'CH3:LABel '+'"'+CH3Name+'"'
        inst.write(temp)
        print(temp)
    if CH4Name != '':
        temp = 'CH4:LABel '+'"'+CH4Name+'"'
        inst.write(temp)
        print(temp)
    inst.close()

def setLabelForTek5k():
    inst = vxi11.Instrument(OSCIP)
    if CH1Name != '':
        temp = 'CH1:LABel:NAMe '+'"'+CH1Name+'"'
        inst.write(temp)
        print(temp)
    if CH2Name != '':
        temp = 'CH2:LABel:NAMe '+'"'+CH2Name+'"'
        inst.write(temp)
        print(temp)
    if CH3Name != '':
        temp = 'CH3:LABel:NAMe '+'"'+CH3Name+'"'
        inst.write(temp)
        print(temp)
    if CH4Name != '':
        temp = 'CH4:LABel:NAMe '+'"'+CH4Name+'"'
        inst.write(temp)
        print(temp)
    inst.close()


def pressConnect():
    global OSCIP #示波器IP地址
    global PCIP  #本地IP地址
    global OSCPN #示波器型号
    global ConnFlag #示波器连接状态
    OSCIP = 'TCPIP::'+window.Element('OSCIP').get()+'::INSTR'
    PCIP = 'HARDCopy:PRINTer:ADD "labprn2", "", "'+window.Element('PCIP').get()+'"'
    try:
        inst = vxi11.Instrument(OSCIP)
        inst.ask('*IDN?')
        inst.close()
    except:
        window.Element('TCONN').Update('连接失败')
        ConnFlag = 0
        print('connected failed. Please check your IP and Device')
    else:
        window.Element('TCONN').Update('已连接')
        ConnFlag = 1
        inst = vxi11.Instrument(OSCIP)
        inst.write('*IDN?')
        OSCPN = inst.read().split(',')[1]
        print('connected with '+OSCPN)
        OSCPN = OSCPN[0:4]
        print(OSCPN)

def pressPathF():
    fileFullPath = window.Element('pathF').get()
    (filePath, fileName) = os.path.split(fileFullPath)
    window.Element('pathF').Update(value=filePath)
    window.Element('saveF').Update(value=fileName)
	
def pressSave():
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        saveForTek5k()
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        saveForTek3k()	
		
		
def pressDoL():
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        setLabelForTek5k()
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        setLabelForTek3k()
	
def pressDoA():
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst = vxi11.Instrument(OSCIP)
        inst.write('HORizontal:MODE constant')
        if scale != '':
            temp = 'HORizontal:MODE:SCAle '+scale
            inst.write(temp)
        if recordLength != '':
            temp = 'HORizontal:MODE:RECOrdlength '+recordLength
            inst.write(temp)
        if sampleRate != '':
            temp = 'HORizontal:MODE:SAMPLERate '+sampleRate
            inst.write(temp)
        inst.close()
        print(temp)
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst = vxi11.Instrument(OSCIP)
        if scale != '':
            temp = 'HORizontal:SCAle '+scale
            inst.write(temp)
        if recordLength != '':
            temp = 'HORizontal:RECOrdlength '+recordLength
            inst.write(temp)
        if sampleRate != '':
            temp = 'HORizontal:SAMPLERate '+sampleRate
            inst.write(temp)
        inst.close()
        print(temp)


def pressDoT():
    inst = vxi11.Instrument(OSCIP)
    if source != '':
        temp = 'TRIGGER:A:EDGE:SOURCE '+source
        inst.write(temp)
    if edge != '':
        temp = 'TRIGger:A:EDGE:SLOpe '+edge
        inst.write(temp)
    inst.close()
    print(temp)	

def pressWrite(command):
    inst = vxi11.Instrument(OSCIP)
    if command != '':
        value = command.split('>>')
        if value[0] == 'wait':
            print('wait 2s')
            window.refresh()
            time.sleep(2)
        elif value[0] == 'save':
            scriptSave(value[1])
        elif value[0] == '#':
            pass
        elif value[0] == 'rise':
            scriptMeasRise(value[1])
        elif value[0] == 'fall':
            scriptMeasFall(value[1])
        elif value[0] == 'freq':
            scriptMeasFreq(value[1])
        elif value[0] == 'high':
            scriptMeasVHigh(value[1])
        elif value[0] == 'low':
            scriptMeasVLow(value[1])
        elif value[0] == 'time':
            scriptTime(value[1], value[2])
        elif value[0] == 'data':
            scriptData(value[1], value[2])
        elif value[0] == 'delay':
            scriptMeasDelay(value[1], value[2], value[3], value[4])
        elif value[0] == 'label':
            scriptSetLabel(value[1], value[2])
        else:
            inst.write(value[0])        
            print(value[0])
    inst.close()

def pressRead():
    inst = vxi11.Instrument(OSCIP)
    print(inst.read())
    inst.close()

def pressQuery(command):
    inst = vxi11.Instrument(OSCIP)
    if command != '':
        print(inst.ask(command))
    inst.close()
	
def pressMeasGate():
    inst = vxi11.Instrument(OSCIP)
    if window.Element('measGate').get() != '':
        temp = 'MEASUrement:GATing '+window.Element('measGate').get()
        inst.write(temp)
    inst.close()
    print(temp)	

def pressRun(scriptFile):
    inst = vxi11.Instrument(OSCIP)
    script = open(scriptFile)
    for line in script.readlines():
        if line not in ['\n','\r\n']:
            line = line.strip('\n')
            value = line.split('>>')
            if value[0] == 'wait':
                print('wait 2s')
                window.refresh()
                time.sleep(2)
            elif value[0] == 'save':
                scriptSave(value[1])
            elif value[0] == '#':
                pass
            elif value[0] == 'rise':
                scriptMeasRise(value[1])
            elif value[0] == 'fall':
                scriptMeasFall(value[1])
            elif value[0] == 'freq':
                scriptMeasFreq(value[1])
            elif value[0] == 'high':
                scriptMeasVHigh(value[1])
            elif value[0] == 'low':
                scriptMeasVLow(value[1])
            elif value[0] == 'time':
                scriptTime(value[1], value[2])
            elif value[0] == 'data':
                scriptData(value[1], value[2])
            elif value[0] == 'delay':
                scriptMeasDelay(value[1], value[2], value[3], value[4])
            elif value[0] == 'label':
                scriptSetLabel(value[1], value[2])
            else:
                inst.write(value[0])
                print(line)
                window.refresh()
    print('run successfully')
    inst.close()
	

def scriptSave(fileName):
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst = vxi11.Instrument(OSCIP)
        inst.write('HARDCOPY:PORT FILE')
        inst.write('HARDCOPY:FILENAME "C:/Windows/temp"')
        inst.write('Hardcopy start')
        time.sleep(0.5)
        inst.write('filesystem:readfile "C:/Windows/temp.png"')
        image = inst.read_raw()
        filePath = window.Element('pathF').get()
        temp = filePath+'/'+fileName+".png"
        print('save to:'+temp)
        my_file = open( temp , "wb")
        my_file.write(image)
        inst.write('FILESystem:DELEte "C:/Windows/temp.png"')		
        inst.close()
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst = vxi11.Instrument(OSCIP)
        inst.write(PCIP)
        inst.write('HARDCopy:ACTIVeprinter "labprn2"')
        inst.write('Hardcopy start')
        image = inst.read_raw()
        filePath = window.Element('pathF').get()
        temp = filePath+'/'+fileName+".png"
        print('save to:'+temp)
        my_file = open( temp , "wb")
        my_file.write(image)
        my_file.close()
        inst.close()
    window.refresh()
	
def scriptMeasRise(ch1):
    inst = vxi11.Instrument(OSCIP)
    inst.write('MEASUrement:MEAS1:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS1:TYPe rise')
    inst.write('MEASUrement:MEAS1:STATE on')
    inst.write('MEASUrement:MEAS2:STATE OFF')
    inst.write('MEASUrement:MEAS3:STATE OFF')
    inst.write('MEASUrement:MEAS4:STATE OFF')
    inst.write('MEASUrement:MEAS5:STATE OFF')
    inst.write('MEASUrement:MEAS6:STATE OFF')
    inst.write('MEASUrement:MEAS7:STATE OFF')
    inst.write('MEASUrement:MEAS8:STATE OFF')
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst.write('MEASUrement:ANNOTation:STATE meas1')
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst.write('MEASUrement:INDICators:STATE off')
        inst.write('MEASUrement:INDICators:STATE meas1')
    inst.close()

def scriptMeasFall(ch1):
    inst = vxi11.Instrument(OSCIP)
    inst.write('MEASUrement:MEAS1:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS1:TYPe fall')
    inst.write('MEASUrement:MEAS1:STATE on')
    inst.write('MEASUrement:MEAS2:STATE OFF')
    inst.write('MEASUrement:MEAS3:STATE OFF')
    inst.write('MEASUrement:MEAS4:STATE OFF')
    inst.write('MEASUrement:MEAS5:STATE OFF')
    inst.write('MEASUrement:MEAS6:STATE OFF')
    inst.write('MEASUrement:MEAS7:STATE OFF')
    inst.write('MEASUrement:MEAS8:STATE OFF')
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst.write('MEASUrement:ANNOTation:STATE meas1')
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst.write('MEASUrement:INDICators:STATE off')
        inst.write('MEASUrement:INDICators:STATE meas1')
    inst.close()

def scriptMeasFreq(ch1):
    inst = vxi11.Instrument(OSCIP)
    inst.write('MEASUrement:MEAS1:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS1:TYPe FREQuency')
    inst.write('MEASUrement:MEAS2:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS2:TYPe PERIod')
    inst.write('MEASUrement:MEAS3:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS3:TYPe PWIdth')
    inst.write('MEASUrement:MEAS4:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS4:TYPe pduty')
    inst.write('MEASUrement:MEAS1:STATE on')
    inst.write('MEASUrement:MEAS2:STATE On')
    inst.write('MEASUrement:MEAS3:STATE On')
    inst.write('MEASUrement:MEAS4:STATE On')
    inst.write('MEASUrement:MEAS5:STATE OFF')
    inst.write('MEASUrement:MEAS6:STATE OFF')
    inst.write('MEASUrement:MEAS7:STATE OFF')
    inst.write('MEASUrement:MEAS8:STATE OFF')
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst.write('MEASUrement:ANNOTation:STATE meas1')
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst.write('MEASUrement:INDICators:STATE off')
        inst.write('MEASUrement:INDICators:STATE meas1')
    inst.close()
	
def scriptMeasVHigh(ch1):
    inst = vxi11.Instrument(OSCIP)
    inst.write('MEASUrement:MEAS1:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS1:TYPe High')
    inst.write('MEASUrement:MEAS2:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS2:TYPe MAXimum')
    inst.write('MEASUrement:MEAS1:STATE on')
    inst.write('MEASUrement:MEAS2:STATE On')
    inst.write('MEASUrement:MEAS3:STATE OFF')
    inst.write('MEASUrement:MEAS4:STATE OFF')
    inst.write('MEASUrement:MEAS5:STATE OFF')
    inst.write('MEASUrement:MEAS6:STATE OFF')
    inst.write('MEASUrement:MEAS7:STATE OFF')
    inst.write('MEASUrement:MEAS8:STATE OFF')
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst.write('MEASUrement:ANNOTation:STATE meas1')
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst.write('MEASUrement:INDICators:STATE off')
        inst.write('MEASUrement:INDICators:STATE meas1')
    inst.close()

def scriptMeasVLow(ch1):
    inst = vxi11.Instrument(OSCIP)
    inst.write('MEASUrement:MEAS1:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS1:TYPe low')
    inst.write('MEASUrement:MEAS2:SOUrce1 '+ch1)
    inst.write('MEASUrement:MEAS2:TYPe minimum')
    inst.write('MEASUrement:MEAS1:STATE on')
    inst.write('MEASUrement:MEAS2:STATE On')
    inst.write('MEASUrement:MEAS3:STATE OFF')
    inst.write('MEASUrement:MEAS4:STATE OFF')
    inst.write('MEASUrement:MEAS5:STATE OFF')
    inst.write('MEASUrement:MEAS6:STATE OFF')
    inst.write('MEASUrement:MEAS7:STATE OFF')
    inst.write('MEASUrement:MEAS8:STATE OFF')
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst.write('MEASUrement:ANNOTation:STATE meas1')
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst.write('MEASUrement:INDICators:STATE off')
        inst.write('MEASUrement:INDICators:STATE meas1')
    inst.close()
	
def scriptTime(name, ch1):
    scriptMeasRise(ch1)
    time.sleep(2)
    scriptSave(name+'_rise')
    time.sleep(2)
    scriptMeasFall(ch1)
    time.sleep(2)
    scriptSave(name+'_fall')
    time.sleep(2)
    scriptMeasFreq(ch1)
    time.sleep(2)
    scriptSave(name+'_freq')
    time.sleep(2)
    scriptMeasVHigh(ch1)
    time.sleep(2)
    scriptSave(name+'_Vhigh')
    time.sleep(2)
    scriptMeasVLow(ch1)
    time.sleep(2)
    scriptSave(name+'_Vlow')
    time.sleep(2)
	
def scriptData(name, ch1):
    scriptMeasRise(ch1)
    time.sleep(2)
    scriptSave(name+'_rise')
    time.sleep(2)
    scriptMeasFall(ch1)
    time.sleep(2)
    scriptSave(name+'_fall')
    time.sleep(2)
    scriptMeasVHigh(ch1)
    time.sleep(2)
    scriptSave(name+'_Vhigh')
    time.sleep(2)
    scriptMeasVLow(ch1)
    time.sleep(2)
    scriptSave(name+'_Vlow')
    time.sleep(2)

def scriptMeasDelay(ch1, sl1, ch2, sl2):
    inst = vxi11.Instrument(OSCIP)
    inst.write('MEASUrement:MEAS1:TYPe delay')
    inst.write('MEASUrement:MEAS1:SOUrce1 '+ch1)
    inst.write('MEASUREMENT:MEAS1:DELAY:EDGE1 '+sl1)
    inst.write('MEASUrement:MEAS1:SOUrce2 '+ch2)
    inst.write('MEASUREMENT:MEAS1:DELAY:EDGE2 '+sl2)
    inst.write('MEASUrement:MEAS1:DELay:DIRection forwards')
    inst.write('MEASUrement:MEAS1:STATE on')
    inst.write('MEASUrement:MEAS2:STATE Off')
    inst.write('MEASUrement:MEAS3:STATE OFF')
    inst.write('MEASUrement:MEAS4:STATE OFF')
    inst.write('MEASUrement:MEAS5:STATE OFF')
    inst.write('MEASUrement:MEAS6:STATE OFF')
    inst.write('MEASUrement:MEAS7:STATE OFF')
    inst.write('MEASUrement:MEAS8:STATE OFF')
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst.write('MEASUrement:ANNOTation:STATE meas1')
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst.write('MEASUrement:INDICators:STATE off')
        inst.write('MEASUrement:INDICators:STATE meas1')
    inst.close()
	
def scriptSetLabel(CH1, CH1Name):
    if OSCPN in ('DPO5', 'DPO7', 'MSO5', 'DSA7', 'DSO7'):
        inst = vxi11.Instrument(OSCIP)
        temp = CH1+':LABel:NAMe '+'"'+CH1Name+'"'
        inst.write(temp)
        print(temp)
        inst.close()
    elif OSCPN in ('MDO4', 'MSO4', 'DPO4', 'MDO3'):
        inst = vxi11.Instrument(OSCIP)
        temp = CH1+':LABel '+'"'+CH1Name+'"'
        inst.write(temp)
        print(temp)
        inst.close()
		
while True:
    event, value = window.read()
    window.refresh()
    if event == 'Connect':
        pressConnect()
    elif event == 'pathF':
        if ConnFlag == 1:
            pressPathF()
        else:
            print('Device is not connected')
    elif event == 'save':
        if ConnFlag == 1:
            pressSave()
        else:
            print('Device is not connected')
    elif event == 'doL':
        CH1Name = value[0]
        CH2Name = value[1]
        CH3Name = value[2]
        CH4Name = value[3]        
        if ConnFlag == 1:
            pressDoL()
        else:
            print('Device is not connected')
    elif event == 'doA':
        scale = value[4]
        recordLength = value[5]
        sampleRate = value[6]
        if ConnFlag == 1:
            pressDoA()
        else:
            print('Device is not connected')
    elif event == 'doT':
        source = value[7]
        edge = value[8]
        if ConnFlag == 1:
            pressDoT()
        else:
            print('Device is not connected')
    elif event == 'write':
        window.Element('status').update(background_color='red')
        command = value[9]
        if ConnFlag == 1:
            pressWrite(command)
        else:
            print('Device is not connected')
        window.Element('status').update(background_color='green')
    elif event == 'read':
        if ConnFlag == 1:
            pressRead()
        else:
            print('Device is not connected')
    elif event == 'query':
        command = value[9]
        if ConnFlag == 1:
            pressQuery(command)
        else:
            print('Device is not connected')
    elif event == 'run':
        window.Element('status').update(background_color='red')
        scriptFile = value[10]
        if ConnFlag == 1:
            pressRun(scriptFile)
        else:
            print('Device is not connected')
        window.Element('status').update(background_color='green')
    elif event == 'doM':
        if ConnFlag == 1:
            pressMeasGate()
        else:
            print('Device is not connected')
    elif event in (None, 'Cancel'): 
        break

window.close()
