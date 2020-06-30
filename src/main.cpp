//
//  main.cpp
//  Alekseevskii Conjecture
//
//  Created by Lucas Schuermann on 10/22/13.
//  Copyright (c) 2013 Lucas Schuermann. All rights reserved.
//

#include <pthread.h>
#include <stdio.h>
#include <assert.h>

#include "Blocking.h"

int main()
{
    Blocking blocker = Blocking();
    blocker.iterate();
    
    return 0;
}