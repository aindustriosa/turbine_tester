import machine
import utime

led_onboard = machine.Pin(25, machine.Pin.OUT)
button = machine.Pin(20, machine.Pin.IN, machine.Pin.PULL_UP)
motor = machine.PWM(machine.Pin(15))
flow_count = 0

flow_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)

def flow_int_handler(pin):
    global flow_count
    flow_pin.irq(handler=None)
    #print("interrupt!")
    flow_count=flow_count+1
    flow_pin.irq(handler=flow_int_handler)

flow_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=flow_int_handler)

frequency=1000
motor.freq(frequency)
analog_value = machine.ADC(28)

step=1000
samples=20


while True:
    max_analog=0
    max_flow=0
    print("Waiting for button press to start...")
    flow_count = 0
    flow_last = 0
    while button.value():
        utime.sleep(0.1)
    for duty_cycle in range (0,65535,step):
        led_onboard.toggle()
        motor.duty_u16(duty_cycle)
        utime.sleep(0.25)
        sum=0
        for i in range (1,samples):
            reading = analog_value.read_u16()
            sum = sum+reading
        average=sum/samples
        if (average>max_analog):
            max_analog=average
        if (flow_count>max_flow):
            max_flow=flow_count
        flow_pps=1000*flow_count/(utime.ticks_ms()-flow_last)
        flow_last=utime.ticks_ms()
        print("PWM:",duty_cycle,", ANALOG:",average,", FLOW_PPS:",flow_pps)
        flow_count=0
    print("Test finished!")
    print("Max Analog was",max_analog, "and Max Flow was",max_flow)
    motor.duty_u16(0)
  
