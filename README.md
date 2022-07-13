# TaserKart

Mario Kart but if your character gets hit, you get electricuted


## Plan

Nintendo Switch -> HDMI spitter -> TV (to play on)<br>
                                -> laptop -> Google Colab -(if hit)-> server -> microcontroller -> TENS unit


## Details
- Microcontroller (MC) = Raspberry Pi Pico W
- 1x MC hardwired into TENS unit, can controll output for two players (maybe four?)
- Use GPU in Google Colab to analyse a single player's feed



| Parts  | 2 Players     | 4 Players |
|--------------|-----------|------------|
| Laptop | 1 | 1  |
| CG scripts| 2  |  4  |
|Microcontrollers | 1 | 2 |
|TENS units | 1 | 2 |



## Progress

**Done:**
- MC controlled TENS unit
- MC controlled by server

**To do:**
- Compile new data sets
- Computer vision model
- Combine all the ingredients for two player Taser Kart
- (Upgrade to four player Taser Kart)