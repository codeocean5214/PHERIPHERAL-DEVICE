
import board
import busio
try : 
    import adafruit_bmp280
    import adafruit_dht
    from mlx90614 import MLX90614
except Exception as e:
    print("Error importing sensor libraries: ", e)

class Environment : 
    def __init__(self,dht_pin = board.D4):
        #i2c protocol is inter integrated circuit protocol 
        #it is used to connect devices to rspi okay then we use intialisze and define the pheripherals 
    
        self.i2c = board.I2C()
        try: 
            self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(self.i2c,address=0x76)

        except Exception as e:
            print(f"Error intializing BMP280 sensor: {e}")

        try: 
            self.dht22 = adafruit_dht.DHT22(dht_pin)

        except Exception as e:
            print(f"Error intializing DHT22 sensor: {e}")
        try: 
            self.thermal = MLX90614(self.i2c)

        except Exception as e:
            print(f"Error intializing thermal sensor: {e}")
        
        def get_data(self):
           #intial reading are zero 
            data   = { 
            "room_temp": 0.0,
            "humidity": 0.0,
            "pressure": 0.0,
            "body_temp": 0.0
        }
        #we update one by one 
            if self.dht22 : 
                try : 
                    data["room_temp"] = self.dht22.temperature
                    data["humidity"] = self.dht22.humidity
                except Exception as e: 
                    print(f"Error reading DHT22 sensor: {e}")
            if self.bmp280 : 
                try : 
                    data["pressure"] = self.bmp280.pressure
                   
                except Exception as e: 
                    print(f"Error reading BMP280 sensor: {e}")  
            if self.thermal : 
                try : 
                    data["body_temp"] = self.thermal.get_object_1()
                except Exception as e: 
                    print(f"Error reading thermal sensor: {e}")
            return data
          