<h1 style="font-size: 34px;color: #6167b8;">mlx_init() - mlx_release()</h1>

<blockquote>
  <p>🔹 <strong>1.</strong> The mlx_init function will create this connection. No parameters are needed, ant it will return a void * identifier, used for further calls to the library routines. The mlx_release function can be used at the end of the program to disconnect from the graphic system and release resources.</p>
</blockquote>

<blockquote>
  <p>🔹 <strong>2.</strong> <code>mlx_init()</code> must be called before any other mlx function, and <code>mlx_release()</code> must be called after the game is over.</p>
</blockquote>


<h1 style="font-size: 34px;color: #6167b8;">mlx_new_window() - mlx_destroy_window() - mlx_clear_window()</h1>

<blockquote>
  <p>🔹 
  <strong>  1.  </strong>
   The  mlx_new_window  () function creates a new window on the screen, using the width and height parameters to determine its size, and title as the text
       that should be displayed in the window's title bar.  The mlx_ptr parameter is the connection identifier returned by mlx_init () (see the mlx man page).
       mlx_new_window  ()  returns a void * window identifier that can be used by other MiniLibX calls.  Note that the MiniLibX can handle an arbitrary number
       of separate windows.
 
   </p>
</blockquote>

<blockquote>
  <p>🔹 
  <strong>  2.  </strong>
   mlx_clear_window () and mlx_destroy_window () respectively clear (in black) and destroy the given window. They both have the same  parameters:  mlx_ptr
       is the screen connection identifier, and win_ptr is a window identifier.
 
   </p>
</blockquote>
