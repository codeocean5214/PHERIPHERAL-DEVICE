from gpiozero  import MotionSensor, LED
class SecurityChecks: 
    def __init__(self,pir_pin =17,led_pin=27): 
        #we have made the puu_up false because first it common to be false and prevent it from 
        #going false triggers and also helps in testing

        self.pir = MotionSensor(pir_pin,pull_up = False)
        #whenever the door is lock  is on then self.led = 1 that is high else false 
        self.led = LED(led_pin)
    @property 
    def detected_motion(self): 
        return self.pir.motion_detected
    #we will create two methods one to lock the door and one to unlock the door
    def lock_door(self): 
        self.led.on()
    def unlock_door(self): 
        self.led.off()
    

    