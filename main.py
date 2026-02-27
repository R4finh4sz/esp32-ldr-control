# ============================================================
# SISTEMA DE CONTROLE DE LUMINOSIDADE
# ESP32 + LDR + Relé + 3 LEDs Independentes
# MicroPython
# ============================================================

from machine import Pin, ADC
from time import sleep_ms, ticks_ms, ticks_diff

# ── LDR ─────────────────────────────────────────────────────
# Certifique-se que o fio físico esteja no pino 34
ldr = ADC(Pin(34))
ldr.atten(ADC.ATTN_11DB)
ldr.width(ADC.WIDTH_12BIT)

# ── Relé ────────────────────────────────────────────────────
rele = Pin(26, Pin.OUT)
rele.value(1)  # Começa desligado (Lógica Invertida)

# ── LEDs Independentes ──────────────────────────────────────
# Ajustado pino 13 para o Verde para evitar conflito com botão no 14
led_vermelho = Pin(12, Pin.OUT)
led_azul     = Pin(27, Pin.OUT)
led_verde    = Pin(13, Pin.OUT) 

# ── Botão físico ────────────────────────────────────────────
botao = Pin(14, Pin.IN, Pin.PULL_UP)

# ============================================================
# CONSTANTES
# ============================================================
LIMIAR_ESCURO = 3000  # Escuro -> Vermelho + Relé ON
LIMIAR_MEDIO  = 1500  # Médio  -> Verde
                      # Alto   -> Azul

DEBOUNCE_MS          = 200
INTERVALO_LEITURA_MS = 500

# ============================================================
# VARIÁVEIS DE ESTADO
# ============================================================
sistema_ativo    = True
ultimo_botao_ms  = 0
estado_botao_ant = 1

# ============================================================
# FUNÇÕES DE CONTROLE DOS LEDS
# ============================================================

def apagar_leds():
    """Apaga todos os LEDs."""
    led_vermelho.value(0)
    led_verde.value(0)
    led_azul.value(0)

def set_nivel(valor_adc):
    """Define LEDs e Relé conforme a luminosidade."""
    apagar_leds()
    
    if valor_adc >= LIMIAR_ESCURO:
        # BAIXO (Escuro) -> LED Vermelho + LIGA relé
        led_vermelho.value(1)
        rele.value(0) 
        return "BAIXO (Escuro) | Lâmpada: LIGADA"

    elif valor_adc >= LIMIAR_MEDIO:
        # MÉDIO -> LED Verde + DESLIGA relé
        led_verde.value(1)
        rele.value(1)
        return "MÉDIO          | Lâmpada: DESLIGADA"

    else:
        # ALTO (Claro) -> LED Azul + DESLIGA relé
        led_azul.value(1)
        rele.value(1)
        return "ALTO (Claro)   | Lâmpada: DESLIGADA"

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def checar_botao():
    global sistema_ativo, ultimo_botao_ms, estado_botao_ant
    estado_atual = botao.value()
    agora = ticks_ms()

    if estado_atual == 0 and estado_botao_ant == 1:
        if ticks_diff(agora, ultimo_botao_ms) > DEBOUNCE_MS:
            ultimo_botao_ms = agora
            sistema_ativo = not sistema_ativo
            if sistema_ativo:
                print("[BOTÃO] Sistema ATIVADO")
            else:
                apagar_leds()
                rele.value(1)
                print("[BOTÃO] Sistema PAUSADO")
    estado_botao_ant = estado_atual

def ler_ldr_media(amostras=5):
    total = 0
    for _ in range(amostras):
        total += ldr.read()
        sleep_ms(10)
    return total // amostras

# ============================================================
# EXECUÇÃO
# ============================================================
print("Sistema Iniciado...")

ultima_leitura_ms = 0

while True:
    agora = ticks_ms()
    checar_botao()

    if ticks_diff(agora, ultima_leitura_ms) >= INTERVALO_LEITURA_MS:
        ultima_leitura_ms = agora
        if sistema_ativo:
            valor = ler_ldr_media()
            status = set_nivel(valor)
            print(f"[LDR] {valor:4d} | {status}")
        else:
            print("[INFO] Sistema pausado.")

    sleep_ms(20)
