# esp32-ldr-control

Sistema de controle de luminosidade utilizando ESP32 + sensor LDR, relé e 3 LEDs independentes.
Desenvolvido em MicroPython, o sistema aciona automaticamente uma lâmpada em ambientes escuros
e utiliza LEDs coloridos para indicar o nível de luminosidade atual.

---

## Funcionalidades

- Controle automático de lâmpada via relé baseado na luz ambiente
- 3 LEDs independentes indicando níveis baixo, médio e alto de luminosidade
- Botão físico para pausar/retomar o sistema com debounce por software
- Leituras do LDR com média de 5 amostras para reduzir ruído do ADC
- Loop principal leve (20ms de sleep) garantindo alta responsividade do botão

---

## Hardware

| Componente          | GPIO  | Observações                        |
|---------------------|-------|------------------------------------|
| LDR (analógico)     | 34    | ADC1 — resistor pull-down de 10kΩ  |
| Relé                | 26    | Lógica invertida: LOW = LIGADO     |
| LED Vermelho (baixo)| 12    | Resistor de 330Ω obrigatório       |
| LED Verde (médio)   | 13    | Resistor de 330Ω obrigatório       |
| LED Azul (alto)     | 27    | Resistor de 330Ω obrigatório       |
| Botão físico        | 14    | PULL_UP interno habilitado         |

---

## Níveis de Luminosidade

| Nível         | Valor ADC   | LED          | Relé (Lâmpada) |
|---------------|-------------|--------------|----------------|
| Baixo (escuro)| ≥ 3000      | 🔴 Vermelho   | ✅ LIGADA       |
| Médio         | 1500 – 2999 | 🟢 Verde      | ❌ Desligada    |
| Alto (claro)  | < 1500      | 🔵 Azul       | ❌ Desligada    |

---

## Conexões

