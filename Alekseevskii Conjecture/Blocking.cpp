//
//  Blocking.cpp
//  Alekseevskii Conjecture
//
//  Created by Lucas Schuermann on 11/12/13.
//  Copyright (c) 2013 Lucas Schuermann. All rights reserved.
//

#include "Blocking.h"

Blocking::Blocking()
{
    sideLength = BLOCKING_SIDE_LENGTH;
    sphereBound = sqrt(90)/2*sideLength;
    max = Vector90();
    min = Vector90();
}

Blocking::~Blocking()
{
    blocks.clear();
}

std::vector<Vector90> Blocking::iterate()
{
    Vector90 start = Vector90();
    start[IND(1,2,1)] = start[IND(1,2,2)] = start[IND(1,3,1)] = start[IND(1,3,3)] = start[IND(2,3,2)]
        = start[IND(2,3,3)] = 0;
    start[IND(1,2,3)] = start[IND(1,3,2)] = 1.0 / sqrt(6.0);
    start[IND(2,3,1)] = - 1.0 / sqrt(6.0);
    for(int i = 4; i <= 6; i++)
        for(int j = i+1; j <= 6; j++)
            for(int k = 4; k <= 6; k++)
                start[IND(i,j,k)] = start[IND(i-3,j-3,k-3)];
    
    for(int i = 0; i < 90; i++)
        printf("%f\n", start[i]);
    blocks.push_back(start);
    
    unsigned long checked = 0;
    while(true)
    {
        if(checked >= blocks.size())
            break;
        else
        {
            Vector90 b = blocks[checked];
            addBlocksFrom(b);
            checked++;
        }
    }
    
    return blocks;
}

void Blocking::addBlocksFrom(Vector90 block)
{
    for(int side = 0; side < 180; side++)
    {
        Vector90 delta = Vector90();
        if(side < 90)
        {
            delta[side] = sideLength;
        }
        else
        {
            delta[side-90] = -sideLength;
        }
        
        Vector90 b = Vector90::add(block, delta);
        if(!checkObjectCondition(b))
        {
            if(!checkRedundancy(b))
            {
                blocks.push_back(b);
            }
        }
    }
}

bool Blocking::checkRedundancy(Vector90 block)
{
    for(int i = 0; i < blocks.size(); i++)
        if(block == blocks[i])
            return true;
    
    return false;
}

double Blocking::getMax(int i, int j, int k)
{
    if((i<=6)&&(j<=6)&&(k<=6)&&(i<j))
        return max[IND(i,j,k)];
    else
        return 0.0;
}

double Blocking::getMin(int i, int j, int k)
{
    if((i<=6)&&(j<=6)&&(k<=6)&&(i<j))
        return min[IND(i,j,k)];
    else
        return 0.0;
}

bool Blocking::checkObjectCondition(Vector90 block)
{
    // find max and min for interval computation of conditions
    for(int i = 0; i < 90; i++)
    {
        max[i] = block[i] + sideLength;
        min[i] = block[i] - sideLength;
    }
    
    // unimodular condition
    double uniMax = 0.0;
    double uniMin = 0.0;
    for(int i = 1; i <= 6; i++)
        for(int j = i+1; j <= 6; j++)
        {
            uniMax += getMax(i,j,j);
            uniMin += getMin(i,j,j);
        }
    if(!((0 >= uniMin) && (0 <= uniMax)))
        return false;
    
    // sphere condition
    double sum = 0.0;
    for(int i = 0; i < 90; i++)
        sum += pow(block[i], 2.0);
    double magnitude = sqrt(sum);
    if(!((1.0 >= (magnitude - sphereBound)) && (1.0 <= (magnitude + sphereBound))))
        return false;
    
    // jacobi condition
    double jacMax, jacMin;
    for(int k = 1; k <= 6; k++)
        for(int i = 1; i <= 6; i++)
            for(int j = i+1; j <= 6; j++)
            {
                jacMax = jacMin = 0.0;
                for(int l = 1; l <= 6; l++)
                    for(int m = 1; m <= 6; m++)
                    {
                        jacMax += getMax(i,j,m)*getMax(m,k,l)+getMax(j,k,m)*getMax(m,i,l)+getMax(k,i,m)*getMax(m,j,l);
                        jacMin += getMin(i,j,m)*getMin(m,k,l)+getMin(j,k,m)*getMin(m,i,l)+getMin(k,i,m)*getMin(m,j,l);
                    }
                
                if(!((0 >= jacMin) && (0 <= jacMax)))
                    return false;
            }
    
    // einstein condition
    
    
    return true;
}


