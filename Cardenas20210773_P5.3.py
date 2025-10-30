# -*- coding: utf-8 -*-
"""
Created 

@author: Kecam
"""

"""
Práctica 3: Sistema muscoesqueletico

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Kenia Cardenas Manzo
Número de control: 20210773
Correo institucional: kenia.cardenas201@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
n = round((tend-t0)/dt) + 1
t = np.linspace(t0,tend,n)
u2 = np.zeros(n); u2[round(1/dt):round(2/dt)] = 1

# Componentes del circuito RC y función de transferencia
R,Cs,Cp,A,Z = 100,10E-6,100E-6,0.25,10E3
num = [Cs*R,1-A]
den = [R*(Cs+Cp),1]
sys = ctrl.tf(num,den)
numctrl = [Cs*Z,1-A]
denctrl = [Z*(Cs+Cp),1]
sysctrl = ctrl.tf(numctrl,denctrl)
print(f"Función de transferencia del sistema: {sys}")
print(f"Función de transferencia del sistema con controlador PI: {sysctrl}")

# Componentes del controlador
kP,kI = 0.072751,171448.1808
def controlador(kP,kI,sys):
    Cr = 1E-6
    Re = 1/(kI*Cr)
    Rr = kP*Re
    numPI = [Rr*Cr,1]
    denPI = [Re*Cr,0]
    C = ctrl.tf(numPI,denPI)
    return C

# Controlador PI
C = controlador(kP,kI,sys)

# Sistema PI 
sysPI = ctrl.feedback(ctrl.series(C,sys), 1, sign=-1)

# Respuesta del sistema
_, Fu = ctrl.forced_response(sysctrl, t, u2, x0)  
_, Fsu2 = ctrl.forced_response(sys, t, u2, x0)     
_, Fsu3 = ctrl.forced_response(sysPI, t, Fsu2, x0)   

# Colores
clr1 = np.array([119,190,240])/255
clr2 = np.array([255,203,97])/255
clr6 = np.array([255,137,79])/255
clr4 = np.array([234,91,111])/255

# === FIGURA 1: LAZO ABIERTO ===
fg1 = plt.figure()
plt.plot(t,u2,'-',color=clr1,label='F(t): Pulso')
plt.plot(t,Fsu2,'-',color=clr2,label='Fs1(t): Control')
plt.plot(t,Fu,'-',color=clr6,label='Fs2(t): Caso')
plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t [s]')
plt.ylabel('F(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.21),loc='center',ncol=3)
plt.tight_layout()
plt.show()
fg1.set_size_inches(w,h)
fg1.savefig('sistema_muscoesqueletico_Abierto_python.png',dpi=600,bbox_inches='tight')
fg1.savefig('sistema_muscoesqueletico_Abierto_python.pdf',dpi=600,bbox_inches='tight')

# === FIGURA 2: LAZO CERRADO (TRATAMIENTO SIGUE AL CASO) ===
fg2 = plt.figure()
plt.plot(t,u2,'-',color=clr1,label='F(t): Pulso')
plt.plot(t,Fsu2,'-',color=clr2,label='Fs1(t): Control')
plt.plot(t,Fu,'-',color=clr6,label='Fs2(t): Caso')
plt.plot(t,Fsu3,'--',color=clr4,label='Fs3(t): Tratamiento')
plt.grid(False)
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.1); plt.yticks(np.arange(0,1.2,0.1))
plt.xlabel('t [s]')
plt.ylabel('F(t) [V]')
plt.legend(bbox_to_anchor=(0.5,-0.25),loc='center',ncol=3)
plt.tight_layout()
plt.show()
fg2.set_size_inches(w,h)
fg2.savefig('sistema_muscoesqueletico_Cerrado_python.png',dpi=600,bbox_inches='tight')
fg2.savefig('sistema_muscoesqueletico_Cerrado_python.pdf',dpi=600,bbox_inches='tight')


