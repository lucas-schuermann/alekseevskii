//
//  Common.h
//  Alekseevskii Conjecture
//
//  Created by Lucas Schuermann on 11/12/13.
//  Copyright (c) 2013 Lucas Schuermann. All rights reserved.
//

#ifndef Alekseevskii_Conjecture_Common_h
#define Alekseevskii_Conjecture_Common_h

#define PROFILING true
#define BLOCKING_SIDE_LENGTH 1.0

#include <vector>
#include <map>
#include <math.h>
#include <ctime>
#include <pthread.h>

inline int IND(int i, int j, int k)
{
    return (j-i)+5+5*(i-2)-(1/2)*(i-1)*(i-2)+16*(k-1);
}

class Vector90
{
public:
    Vector90()
    {
        x = new double[90];
    }
    
    Vector90(double initialValue)
    {
        x = new double[90];
        for(int i = 0; i < 90; i++)
        {
            x[i] = initialValue;
        }
    }
    
    double& operator[](int i)
    {
        return x[i];
    }
    
    bool operator==(Vector90 &v)
    {
        for(int i = 0; i < 90; i++)
            if(this->x[i] != v.x[i])
                return false;
        return true;
    }
    
    double get(int index)
    {
        return x[index];
    }
    
    void set(int index, double value)
    {
        x[index] = value;
    }
    
    static Vector90 add(Vector90 vec1, Vector90 vec2)
    {
        Vector90 tmp = Vector90();
        for(int i = 0; i < 90; i++)
        {
            tmp.set(i, vec1.get(i) + vec2.get(i));
        }
        return tmp;
    }
    
private:
    double* x;
};

#endif
