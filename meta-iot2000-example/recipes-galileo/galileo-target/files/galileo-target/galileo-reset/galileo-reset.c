/* 
 * Application listens to galileo reset pin.
 * If pressed it terminates the clloader application.
 *
 * Copyright(c) 2013 Intel Corporation.
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms and conditions of the GNU General Public License,
 * version 2, as published by the Free Software Foundation.
 *
 * This program is distributed in the hope it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
 * more details.
 */



#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/select.h>
#include <signal.h>
#include <sys/wait.h>
#include <ctype.h>
#include <errno.h>
#include <getopt.h>
#include <unistd.h>
#include <string.h>


#include "galileo-reset.h"

int gpio_fd;
fd_set fs_except_set;
int ret;
unsigned char gpio_value;
unsigned char gpio_initial_value;
int reset_active=0;


int main(int argc, char * argv[])
{
    
    char gpio_str[GPIO_STRING_LEN];
    int Verbose=0;
    int arg;
    int input_gpio = -1, output_gpio = -1;

    while ((arg = getopt(argc, argv, ":vi:o:")) != -1) {
	    switch (arg) {
	    case 'i':
		    /* Set the GPIO for reset input signal from shield */
		    input_gpio = atoi(optarg);
		    break;
	    case 'o':
		    /* Set the GPIO for reset output signal to shield */
		    output_gpio = atoi(optarg);
		    break;
	    case 'v':
		    Verbose++;
		    break;
	    default:
		    break;
	    }/* switch(arg) */
    }

    if ((input_gpio < 0) && (output_gpio < 0)) {
            input_gpio = 63;
            output_gpio = 47;
    }

    if (input_gpio < 0){
	    printf("Shield reset input GPIO invalid or not specified (%d)\n", input_gpio);
	    exit(1);
    }
    if (output_gpio < 0){
	    printf("Shield reset output GPIO invalid or not specified (%d)\n", output_gpio);
	    exit(1);
    }

    /*
     * Sheld output reset
     */
    
    sprintf(gpio_str,"echo  %d  > %s ", output_gpio , GPIO_SYS_EXPORT_STRING);
    if (Verbose >=2 )
      printf("Exec:%s\n",gpio_str);
    system(gpio_str);
    
    //  set   /sys/class/gpio/gpioN/direction out
    sprintf(gpio_str,"echo out > %s/gpio%d/direction ", GPIO_SYS_BASE_STRING, output_gpio);
    if (Verbose >=2 )
      printf("Exec:%s\n",gpio_str);
    system(gpio_str);
    
    /*
     * Set sheld reset line low/high to reset all shields
     */
    
    sprintf(gpio_str,"echo 0 > %s/gpio%d/value ", GPIO_SYS_BASE_STRING, output_gpio);
    if (Verbose >=2 )
      printf("Exec:%s\n",gpio_str);
    system(gpio_str);
    sprintf(gpio_str,"echo 1 > %s/gpio%d/value ", GPIO_SYS_BASE_STRING, output_gpio);

    if (Verbose >=2 )
      printf("Exec:%s\n",gpio_str);
    system(gpio_str);
    
            
    sprintf(gpio_str,"echo  %d  > %s ", input_gpio, GPIO_SYS_EXPORT_STRING);
    if (Verbose >=2 )
      printf("Exec:%s\n",gpio_str);
    system(gpio_str);
    

   //    /sys/class/gpio/gpioN/direction in
    
    sprintf(gpio_str,"echo in > %s/gpio%d/direction ", GPIO_SYS_BASE_STRING, input_gpio);
    if (Verbose >=2 )
      printf("Exec:%s\n",gpio_str);
    system(gpio_str);

  
   //    /sys/class/gpio/gpioN/edge both
   // falling only not supported by cy8c9540a driver
    sprintf(gpio_str,"echo both > %s/gpio%d/edge ", GPIO_SYS_BASE_STRING, input_gpio);
    if (Verbose >=2 )
   	printf("Exec:%s\n",gpio_str);
    system(gpio_str);
           
    
    sprintf(gpio_str,"%s/gpio%d/value", GPIO_SYS_BASE_STRING, input_gpio);
    if (Verbose >=2 )
      printf("Opening for select:%s\n",gpio_str);

    gpio_fd = open(gpio_str,O_RDWR);
    if( gpio_fd < 0 ) {
        /* no file found */
        fprintf(stderr,"Failed to open:%s\n",gpio_str);
        exit(EXIT_FAILURE);
    }

    lseek(gpio_fd,0,SEEK_SET);
    read(gpio_fd,&gpio_value,1);
    gpio_initial_value=gpio_value;
    if (Verbose >=2 )
      printf("Gpio val:%d\n",gpio_value);


    while(1) {
 
        /* zero */
    	FD_ZERO(&fs_except_set);
        
   	 /* Add elements */
   	 FD_SET(gpio_fd, &fs_except_set);
        
    	ret = select(gpio_fd+1, 0,0,&fs_except_set, 0); /* Max fd + 1 */
    	if (Verbose >=2 )
      	    printf("Select event received : returned:%d\n",ret);
        
	/* Receive bytes */
        switch(ret){
		case -1:
			fprintf(stderr, "critical fault during select errno=%d", errno);
			break;
		case 0:
			/* timeout */
			fprintf(stderr,"select timeout\n");
			break;
		default:
			/* Process data */
			if(FD_ISSET(gpio_fd, &fs_except_set)){
      			    if (Verbose >=2 )
				printf("Select event received : from GPIO interrupt pin\n");
			    lseek(gpio_fd,0,SEEK_SET);
			    read(gpio_fd,&gpio_value,1);
    			    if (Verbose >=2 )
				printf("Gpio val:%d\n",gpio_value);

			    if ( reset_active == 0 ) { 
				  if ( gpio_value != gpio_initial_value) {
				      reset_active = 1; //
    				      if (Verbose)
					  printf("Sketch Reset button pressed:\n");
				  }
			     }
			     else {
				reset_active = 0; 
    				if (Verbose)
				    printf("Sketch Reset button released: Calling %s\n",SKETCH_RESET_RELEASE_SCRIPT);
				system(SKETCH_RESET_RELEASE_SCRIPT);
			     }
			}
        }
   }
    
  return 0;
}

