import sys
import math

def somar(valores):
            soma = 0.0
            for v in valores:
                soma += float(v)
            return soma
            
def calculate_media(valores):
        soma = somar(valores)
        qtd_elementos = len(valores)
        media = soma / float(qtd_elementos)
        return media

####
# Calcular Variancia 
####
def calculate_variancia(valores):
        media = calculate_media(valores)
        soma = 0.0
        variancia = 0.0
 
        for valor in valores:
            soma += math.pow( (float(valor) - media), 2)
        variancia = soma / float( len(valores) )
        return variancia
####
# Calcular Desvio Padrao 
#### 
def calculate_desvio_padrao(valores):
	    
            variancia = calculate_variancia(valores)
            
            return(variancia, math.sqrt(variancia))
         
def selected_rates_var_des(inicio, fim, sample):
    
    lista = []

    for i in range(inicio, fim):
        lista.append(sample[i]["rate"])  


    media = calculate_media(lista)
    variancia, desvio_padrao = calculate_desvio_padrao(lista)
    
    return (variancia, desvio_padrao)



####
# Imprimir erros
###
def print_e(message):
	str(message)
	print('\033[31m' + message + '\033[0;0m')
	
#####
# Imprimir com destaque
###
def print_s(message):
	str(message)
	print('\033[40m'+'\033[1m' + '\033[32m' + message + '\033[0;0m')


print_s("\n========= INICIANDO ANALISADOR DE AMOSTRAS DE TAXA ==========")
print("Formato esperado das amostras: '(hh:mm:ss) ([int]seconds) ([double]rate)'")

#####
# Verifica se parametros foram especificados
####
if(len(sys.argv) < 6):
	print_e("\n====== Erro! Especifique parametros =======")
	print_e("$ python3 " + str(sys.argv[0]) + " <SAMPLES_FILE> <max/min> <time_ms> <initial_interval> <final_interval>")
	print("\nEncerrando.")
	exit()

######
# Verifica se arquivo existe
#####
path_file = sys.argv[1]

file_trace = open(path_file, "r")
file_tmp = "tmp.txt"

######
# Verifica opcao max/min
#####
option = sys.argv[2]
if(option != "max" and option != "min"):
	print_e("\n====== Erro! Opcao invalida =======")
	print_e("Use: 'max' ou 'min'")
	print_e("$ python3 " + str(sys.argv[0]) + " " + path_file + " <max/min> <time_ms>")
	print("\nEncerrando.")
	exit()
	
######
# Verifica time_ms
#####
has_error = 0
time_ms = 0
try:
    time_ms = int(sys.argv[3])
except ValueError:
    has_error = 1

if(has_error or time_ms < 1):
	print_e("\n====== Erro! time_ms invalido: Deve ser inteiro e maior que zero =======")
	print_e("$ python3 " + str(sys.argv[0]) + " " + path_file + " " + option + " <time_ms>")
	print("\nEncerrando.")
	exit()

######
# Verifica initial_interval e transforma para milisegundos
#####
has_error = 0
initial_interval = 0
try:
    initial_interval = str(sys.argv[4])
    initial_interval_ms = (((int(initial_interval[0:2])*60) + int(initial_interval[3:5]))*60 + int(initial_interval[6:-1]))*1000

except ValueError:
    has_error = 1

if(has_error or len(initial_interval) != 8):
	print_e("\n====== Erro! initial_interval invalido: Deve ser string =======")
	print_e("$ python3 " + str(sys.argv[0]) + " " + path_file + " " + option + " <initial_interval>")
	print("\nEncerrando.")
	exit()


######
# Verifica final_interval e transforma para milisegundos
#####
has_error = 0
final_interval = 0
try:
    final_interval = str(sys.argv[5])
    final_interval_ms = (((int(final_interval[0:2])*60) + int(final_interval[3:5]))*60 + int(final_interval[6:-1]))*1000

except ValueError:
    has_error = 1

if(has_error or len(final_interval) != 8):
	print_e("\n====== Erro! final_interval invalido: Deve ser string =======")
	print_e("$ python3 " + str(sys.argv[0]) + " " + path_file + " " + option + " <final_interval>")
	print("\nEncerrando.")
	exit()


#######
# Imprime error para linha de um arquivo
#########
def fileError(line_error, line_text):
	print_e("\n====== Erro! Valor invalido no arquivo =======")
	print_e("Arquivo: " + path_file)
	print_e("Linha " + str(line_error) + " : " + str(line_text)) 
	print("\nEncerrando.")
	exit()

######
# Le arquivo de amostras e retorna lista de amostras
####
def readSamples(file_txt):
	samples = []
	line_count = 0
	for line in file_txt:
		line_count += 1
		line_text = line
		line = line.split()
		sample = {}
		try:
			time = line[0].split(":")
			# transforma hh:mm:ss com (((hh*60) + mm)*60 + ss)*1000
			sample["hour"] = (((int(time[0])*60) + int(time[1]))*60 + int(time[2]))*1000
			sample["seconds"] = int(line[1])
			sample["rate"] = float(line[2])
		except:
			fileError(line_count, line_text)
		samples.append(sample)
	return samples


#######
# Extrai apenas os traces que estão no intervalo de horario informado
#########
def extractTraceFile(file_trace, initial_interval, final_interval):
	
	data_tmp = open(file_tmp, "w")
	lines =  file_trace.readlines()
        
	for line in lines:
		line_list = line.split()
		time = line_list[0].split(":")
		# transforma hh:mm:ss com (((hh*60) + mm)*60 + ss)*1000
		time_ms = (((int(time[0])*60) + int(time[1]))*60 + int(time[2]))*1000
		if(time_ms >= initial_interval_ms and time_ms <= final_interval_ms):
			data_tmp.write(line)
	
	
	file_trace.close()
	data_tmp.close()
	data_tmp = open(file_tmp, "r")
	return(data_tmp)

		
#####
# Executando leitura das amostras
###


print("Extraindo Traces do Horário")

file_txt = extractTraceFile(file_trace, initial_interval, final_interval)

samples = readSamples(file_txt)

print_s("Quantidade de Amostras: " + str(len(samples)))
if(len(samples) < 1):
	exit()

# Pegando primeira amostra
first_sample = samples[0]

# Verifica se existe intervalo para analise

if(first_sample["hour"] + time_ms >= samples[len(samples)-1]["hour"]):
	exit()

# Verifica se existe horario para analise
if(final_interval_ms > samples[len(samples)-1]["hour"]):
	exit()

print("Preparando...")

# soma das taxas dos primeiros time_ms milisegundos
i = 1		# Iterador
rates_count = 1		# Contador de taxas na soma
i0 = 0		# Iterador da primeira taxa na soma
rates_sum = first_sample["rate"]		# Soma das taxas de i0 a i0+rates_count
while(i < len(samples) and first_sample["hour"] + time_ms >= samples[i]["hour"]):
	rates_sum += samples[i]["rate"]
	rates_count += 1
	i += 1

if(rates_sum == 0.0):
	rates_mean = 0.0
else:
	rates_mean = rates_sum / (rates_count)

# media satisfatoria
selected_rates_mean = rates_mean
selected_start = i0
selected_samples_count = rates_count

# Ininciando analise
print("Analizando...")

while(i < len(samples)):

	# Removendo amostra mais antiga
	rates_sum -= samples[i0]["rate"]
	rates_count -= 1
	i0 += 1
	# Agregando novas amostras para o novo intervalo de tempo
	hasUpdate = 0
	while(i < len(samples) and samples[i0]["hour"] + time_ms >= samples[i]["hour"]):
		hasUpdate = 1
		rates_sum += samples[i]["rate"]
		rates_count += 1	
		i += 1
	
	# Verificando se o ultimo intervalo contem o time_ms estipulado
	if(i == len(samples) and (samples[i0]["hour"] + time_ms > samples[i-1]["hour"])):
		hasUpdate = 0

	# Verifica se a media atual eh melhor que a do historico
	if(hasUpdate):		
		rates_mean = rates_sum / (rates_count)
		if(option == "max" and selected_rates_mean < rates_mean):
			selected_rates_mean = rates_mean
			selected_start = i0
			selected_samples_count = rates_count
		elif(option == "min" and selected_rates_mean > rates_mean):
			selected_rates_mean = rates_mean
			selected_start = i0
			selected_samples_count = rates_count


print("Completo!")

def toHour(time):
	millis = time % 1000
	time = (time-millis)/1000
	seconds = time % 60
	time = (time-seconds)/60
	minutes = time % 60
	hours = (time-minutes)/60
	return (str(int(hours)) + ":" + str(int(minutes)) + ":" + str(int(seconds)) + " " + str(int(millis)))

if(option == "max"):
	carac = "Intervalo com taxa maxima: "
else:
	carac = "Intervalo com taxa minima: "

print_s(carac)
print_s("Linha da amostra inicial: " + str(selected_start+1))
print_s("\tHora inicial: " + toHour(samples[selected_start]["hour"]))
print_s("\tId inicial: " + str(samples[selected_start]["seconds"]))
print_s("\tTaxa inicial: " + str(samples[selected_start]["rate"]))

print_s("Linha da amostra final: " + str(selected_start + selected_samples_count))
print_s("\tHora final: " + toHour(samples[selected_start + selected_samples_count-1]["hour"]))
print_s("\tId final: " + str(samples[selected_start + selected_samples_count-1]["seconds"]))
print_s("\tTaxa final: " + str(samples[selected_start + selected_samples_count-1]["rate"]))
variancia, desvio = selected_rates_var_des(selected_start, selected_start + selected_samples_count-1, samples)

print_s("Quantidade de amostras: " + str(selected_samples_count))
print_s("Taxa Media: " + str(selected_rates_mean))
print("Variancia: ",  round(variancia, 2))
print("Desvio Padrao: ",  round(desvio, 2))
print("\nEncerrando.")
print("Desenvolvido por Antonio Cruz Jr")
