import numpy as np

def meyers(T):
   # Saturation vapour pressure calculation from:
   # Goff & Gratch (1946) 
   # water: uncertain below -70 degC
   # ice: good down to -100 degC
   nimey = np.zeros(len(T))
   for i in range(len(nimey)):
      if -37 < T[i] < 0:	
         t = 273.15 + T[i] # Temperature in K
         tboil = 373.15 # At 1 atm in K
         h2otrip = 273.16 # Triple point temperature of water in K
         esl = 10**(-7.90298*(tboil/t-1)+ 5.02808*np.log10(tboil/t) 
		- 1.3816e-7*(10**(11.344*(1-t/tboil))-1) + 
		8.1328e-3*(10**(-3.49149*(tboil/t-1))-1) + 
		np.log10(1013.246))*100	

         esi = 10**(-9.09718*(h2otrip/t-1)-3.56654 * 
		np.log10(h2otrip/t)+0.876793*(1-t/h2otrip) +
		np.log10(6.1071))*100
 
         deles = esl - esi
         nimey[i] = 1e-3*np.exp(12.96*deles/esi - 0.639)
         nimey[i] = nimey[i]*1e+3 # Convert from per cubic cm to per litre 
      else:
         nimey[i] = 0

   return nimey

