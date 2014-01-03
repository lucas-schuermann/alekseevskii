//
//  Blocking.h
//  Alekseevskii Conjecture
//
//  Created by Lucas Schuermann on 11/12/13.
//  Copyright (c) 2013 Lucas Schuermann. All rights reserved.
//

#ifndef __Alekseevskii_Conjecture__Blocking__
#define __Alekseevskii_Conjecture__Blocking__

#include "Common.h"

class Blocking
{
public:
    Blocking();
    ~Blocking();
    
    std::vector<Vector90> iterate();
    
private:
    void addBlocksFrom(Vector90 block);
    bool checkRedundancy(Vector90 block);

    bool checkObjectCondition(Vector90 block);
    Vector90 max;
    Vector90 min;
    double* ric(int i, int j);
    
    double getMax(int i, int j, int k);
    double getMin(int i, int j, int k);
    
    std::vector<Vector90> blocks;
    double sideLength;
    double sphereBound;
};

#endif /* defined(__Alekseevskii_Conjecture__Blocking__) */
