import numpy as np

class Simulation():

    def __init__(self,min,max):

        self.a = min
        self.b = max
        
    def Rest_HR(self):

        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/12)
        s1 = 2.05+np.sin(0.9*((2 * np.pi * t1)+0.8))
        t2 = np.arange(0.0, 1.0, 1/9)
        s2 = 1+np.sin(0.9*((2 * np.pi * t2)+0.8))
        t3 = np.arange(0.0, 1.0, 1/3)
        s3 = 1+1.8*np.sin(2.9*((2 * np.pi * t3)+0.8))

        for i in range(3):

            rand_func1 = np.random.randint(self.b-4, self.b, 12)
            s4 = s1.astype(int) + rand_func1

            rand_func2 = np.random.randint(self.a, self.a+8, 9)
            s5 = s2.astype(int) + rand_func2

            rand_func3 = np.random.randint(self.a+7, self.b, 3)
            s6 = s3.astype(int) + rand_func3
 
            s5 = np.append(s4,s5)
            s6 = np.append(s5,s6)

            self.sf = np.append(self.sf,s6)

        return self.sf

    def Low_HR(self, danger):

        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/12)
        s1 = 2.05+np.sin(0.9*((2 * np.pi * t1)+0.8))
        t2 = np.arange(0.0, 1.0, 1/9)
        s2 = 1+np.sin(0.9*((2 * np.pi * t2)+0.8))
        t3 = np.arange(0.0, 1.0, 1/3)
        s3 = 1+1.8*np.sin(2.9*((2 * np.pi * t3)+0.8))

        for i in range(3):

            if i == 1:
                self.a = 58
                self.b = 73
            elif i == 2:
                self.a = 55
                self.b = 70

            rand_func1 = np.random.randint(self.b-4, self.b, 12)
            s4 = s1.astype(int) + rand_func1

            rand_func2 = np.random.randint(self.a, self.a+8, 9)
            s5 = s2.astype(int) + rand_func2

            rand_func3 = np.random.randint(self.a+7, self.b, 3)
            s6 = s3.astype(int) + rand_func3
 
            s5 = np.append(s4,s5)
            s6 = np.append(s5,s6)

            self.sf = np.append(self.sf,s6)

        if danger == "y":

            HAv = np.random.randint(200,220,3)
            self.sf[12] = HAv[0]
            self.sf[22] = HAv[1]
            self.sf[38] = HAv[2]

        return self.sf
    
    def High_HR(self, danger):

        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/12)
        s1 = 2.05+np.sin(0.9*((2 * np.pi * t1)+0.8))
        t2 = np.arange(0.0, 1.0, 1/9)
        s2 = 1+np.sin(0.9*((2 * np.pi * t2)+0.8))
        t3 = np.arange(0.0, 1.0, 1/3)
        s3 = 1+1.8*np.sin(2.9*((2 * np.pi * t3)+0.8))

        for i in range(3):

            if i == 1:
                self.a = 70
                self.b = 85
            elif i == 2:
                self.a = 85
                self.b = 100

            rand_func1 = np.random.randint(self.b-4, self.b, 12)
            s4 = s1.astype(int) + rand_func1

            rand_func2 = np.random.randint(self.a, self.a+8, 9)
            s5 = s2.astype(int) + rand_func2

            rand_func3 = np.random.randint(self.a+7, self.b, 3)
            s6 = s3.astype(int) + rand_func3
 
            s5 = np.append(s4,s5)
            s6 = np.append(s5,s6)

            self.sf = np.append(self.sf,s6)

        if danger == "y":

            HAv = np.random.randint(200,220,3)
            self.sf[16] = HAv[0]
            self.sf[29] = HAv[0]
            self.sf[42] = HAv[0]

        return self.sf

    def Norm_Temp(self, fever):
    
        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/24)
        s1 = 0.5 + 0.5 * np.sin((1.7 * 2 * np.pi * t1) - 0.7)
        s3 = 0.5 + 0.5 * np.sin((1.5 * 2 * np.pi * t1) - 3.8)

        for i in range(3):

            rand_func1 = np.random.uniform(self.a-0.5, self.a, 7)
            s4 = s1[0:7] + rand_func1

            rand_func2 = np.random.uniform(self.b-0.3, self.b, 7)
            s5 = rand_func2

            rand_func3 = np.random.uniform(self.a-0.5, self.a, 10)
            s6 = s3[14:24] + rand_func3

            s5 = np.append(s4,s5)
            s6 = np.append(s5,s6)

            self.sf = np.append(self.sf,s6)

        if fever == "y":

            HAv = np.random.uniform(37.8,39.2,3)
            self.sf[10] = HAv[0]
            self.sf[24] = HAv[1]
            self.sf[33] = HAv[2]

        return self.sf
    
    def Low_Temp(self):
    
        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/24)
        s1 = 0.5 + 0.5 * np.sin((1.7 * 2 * np.pi * t1) - 0.7)
        s3 = 0.5 + 0.5 * np.sin((1.5 * 2 * np.pi * t1) - 3.8)

        for i in range(3):

            if i == 1:
                self.a = 35.5
                self.b = 36.2
            elif i == 2:
                self.a = 34.5
                self.b = 35.0

            rand_func1 = np.random.uniform(self.a-0.5, self.a, 7)
            s4 = s1[0:7] + rand_func1

            rand_func2 = np.random.uniform(self.b-0.3, self.b, 7)
            s5 = rand_func2

            rand_func3 = np.random.uniform(self.a-0.5, self.a, 10)
            s6 = s3[14:24] + rand_func3

            s5 = np.append(s4,s5)
            s6 = np.append(s5,s6)

            self.sf = np.append(self.sf,s6)

        return self.sf

    def High_Temp(self):
    
        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/24)
        s1 = 0.5 + 0.5 * np.sin((1.7 * 2 * np.pi * t1) - 0.7)
        s3 = 0.5 + 0.5 * np.sin((1.5 * 2 * np.pi * t1) - 3.8)

        for i in range(3):

            if i == 1:
                self.a = 37.5
                self.b = 38.9
            elif i == 2:
                self.a = 38.5
                self.b = 41.5

            rand_func1 = np.random.uniform(self.a-0.5, self.a, 7)
            s4 = s1[0:7] + rand_func1

            rand_func2 = np.random.uniform(self.b-0.3, self.b, 7)
            s5 = rand_func2

            rand_func3 = np.random.uniform(self.a-0.5, self.a, 10)
            s6 = s3[14:24] + rand_func3

            s5 = np.append(s4,s5)
            s6 = np.append(s5,s6)

            self.sf = np.append(self.sf,s6)

        return self.sf

    def Norm_Weig(self):

        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/24)

        s1 = 0.0625*np.sin(6*2 * np.pi * t1)
        s2 = 0.15*np.sin((3*2 * np.pi * t1)-1/2)
        s3 = 0.2*np.sin((2*2 * np.pi * t1)-11/12)
        s4 = 0.125*np.sin((1.2*2 * np.pi * t1)+1/4)

        for i in range(3):

            rand_func1 = np.random.uniform(self.a, self.a+0.25, 3)
            s5 = s1[0:3] + rand_func1

            rand_func2 = np.random.uniform(self.a+0.1, self.a+0.35, 5)
            s6 = s2[0:5] + rand_func2

            rand_func3 = np.random.uniform(self.a+0.15, self.b, 6)
            s7 = s3[1:7] + rand_func3

            rand_func4 = np.random.uniform(self.a+0.125, self.a+0.325, 10)
            s8 = s4[0:10] + rand_func4
       
            s6 = np.append(s5,s6)
            s7 = np.append(s6,s7)
            s8 = np.append(s7,s8)
            self.sf = np.append(self.sf,s8)

        return self.sf

    def Low_Weig(self):

        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/24)

        s1 = 0.0625*np.sin(6*2 * np.pi * t1)
        s2 = 0.15*np.sin((3*2 * np.pi * t1)-1/2)
        s3 = 0.2*np.sin((2*2 * np.pi * t1)-11/12)
        s4 = 0.125*np.sin((1.2*2 * np.pi * t1)+1/4)

        for i in range(3):
            if i == 1:
                self.a = self.a - 0.5
                self.b = self.b - 0.5
            elif i == 2:
                self.a = self.a + 0.7
                self.b = self.b + 0.7
            rand_func1 = np.random.uniform(self.a, self.a+0.25, 3)
            s5 = s1[0:3] + rand_func1

            rand_func2 = np.random.uniform(self.a+0.1, self.a+0.35, 5)
            s6 = s2[0:5] + rand_func2

            rand_func3 = np.random.uniform(self.a+0.15, self.b, 6)
            s7 = s3[1:7] + rand_func3

            rand_func4 = np.random.uniform(self.a+0.125, self.a+0.325, 10)
            s8 = s4[0:10] + rand_func4
       
            s6 = np.append(s5,s6)
            s7 = np.append(s6,s7)
            s8 = np.append(s7,s8)
            self.sf = np.append(self.sf,s8)

        return self.sf

    def High_Weig(self):

        self.sf = []

        t1 = np.arange(0.0, 1.0, 1/24)

        s1 = 0.0625*np.sin(6*2 * np.pi * t1)
        s2 = 0.15*np.sin((3*2 * np.pi * t1)-1/2)
        s3 = 0.2*np.sin((2*2 * np.pi * t1)-11/12)
        s4 = 0.125*np.sin((1.2*2 * np.pi * t1)+1/4)

        for i in range(3):
            if i == 1:
                self.a = self.a + 0.5
                self.b = self.b + 0.5
            elif i == 2:
                self.a = self.a + 0.7
                self.b = self.b + 0.5
            rand_func1 = np.random.uniform(self.a, self.a+0.25, 3)
            s5 = s1[0:3] + rand_func1

            rand_func2 = np.random.uniform(self.a+0.1, self.a+0.35, 5)
            s6 = s2[0:5] + rand_func2

            rand_func3 = np.random.uniform(self.a+0.15, self.b, 6)
            s7 = s3[1:7] + rand_func3

            rand_func4 = np.random.uniform(self.a+0.125, self.a+0.325, 10)
            s8 = s4[0:10] + rand_func4
       
            s6 = np.append(s5,s6)
            s7 = np.append(s6,s7)
            s8 = np.append(s7,s8)
            self.sf = np.append(self.sf,s8)

        return self.sf