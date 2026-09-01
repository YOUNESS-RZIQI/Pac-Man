LIBRARY FUNCTIONS
       First of all, you need to initialize the connection between your software and the graphic and user sub-systems.  Once this completed, you'll be able to use other MiniLibX func‐
       tions to send and receive the messages from the display, like "I want to draw a yellow pixel in this window" or "did the user hit a key?".

       The mlx_init function will create this connection. No parameters are needed, ant it will return a void * identifier, used for further calls to the library routines. The mlx_re‐
       lease function can be used at the end of the program to disconnect from the graphic system and release resources.

       All other MiniLibX functions are described in the following man pages:

       mlx_new_window      : manage windows

       mlx_pixel_put       : draw inside a window

       mlx_new_image       : manipulate images

       mlx_loop            : handle keyboard or mouse events

       mlx_extra           : extra functions available in the MinilibX