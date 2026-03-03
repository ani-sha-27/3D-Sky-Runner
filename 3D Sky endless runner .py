import sys
import random
import os
from math import cos, sin, pi
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#Plane er starting position
#Endless Runner
pln_po_x = 0.0
pln_po_y = 5.0
pln_po_z = 0.0
pln_rota_x = 0.0
pln_rota_y = 0.0
pln_rota_z = 0.0
plane_speed = 1 #Plane er speed bare komay

# Camera position thik kora
came_posi_x = 0.0
came_posi_y = 5.0
came_posi_z = 35.0
came_targe_x = 0.0
came_targe_y = 5.0
came_targe_z = 0.0
came_up_x = 0.0
came_up_y = 1.0
came_up_z = 0.0
camera_mode = 'third_person' 

# Game state
intro_scren = True 
is_gam_strt_ = False
is_gam_over_ = False
score = 0
high_score = 0
is_new_high_score = False #flag diye kora
time_remaining = 60 #timer fixed
countdown_timer = -1 

# Lives system
lives = 3 #player er health koita

# ei objects gula list akare save kora
buildings = []
rings = []
clouds = []
drones = [] 

#Features for sun/clouds
is_sun_visible = False
is_cloud_gray = False


# Model Drawing
def draw_building(pos_x, pos_z, height, width, depth, colors):
    glPushMatrix()
    glTranslated(pos_x, 0, pos_z) 
    
    # buildings gula cube akare save kora
    segment_height = 2.0
    num_segments = int(height / segment_height)
    #building draw
    for i in range(num_segments): #endless cube
        glPushMatrix() #prottek cube er jonno alada alada matrix toiri kore
        glTranslated(0, segment_height * (i + 0.5), 0) #eta diye amra pos_x,pos_y pos e niye jawa hoi
        
        
        if i < len(colors):
            glColor3f(*colors[i])
        else:
            
            glColor3f(0.5, 0.5, 0.5) 

        glScaled(width, segment_height, depth)
        glutSolidCube(1)
        
        #black window
        glColor3f(0.0, 0.0, 0.0)
        window_size = 0.2
        # Front window
        glPushMatrix()
        glTranslated(0, 0, 0.5)
        glScaled(window_size, window_size, 0.1)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslated(0.3, 0, 0.5)
        glScaled(window_size, window_size, 0.1)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslated(-0.3, 0, 0.5)
        glScaled(window_size, window_size, 0.1)
        glutSolidCube(1)
        glPopMatrix()
        
        glPopMatrix()
        
    glPopMatrix()
#ring features or ring draw
def draw_ring(pos_x, pos_y, pos_z, radius, thickness):
    glPushMatrix()
    glTranslated(pos_x, pos_y, pos_z)
    glColor3f(1.0, 0.7, 0.0) #yellow
    glutSolidTorus(thickness, radius, 30, 60) # Increased segments for a smoother look
    glPopMatrix()
    
#Drone Features and draw
def draw_drone(pos_x, pos_y, pos_z, scale):
    glColor3f(0.8, 0.8, 0.8) # Gray body
    glPushMatrix()
    glTranslated(pos_x, pos_y, pos_z)
    glScaled(scale, scale, scale)
    
    # Main body
    glPushMatrix()
    glScaled(3.0, 0.5, 3.0)
    glutSolidCube(1)
    glPopMatrix()
    
    # Propeller arms
    glColor3f(0.3, 0.3, 0.3) 
    glPushMatrix()
    glScaled(0.5, 0.5, 5.0)
    glutSolidCube(1)
    glPopMatrix()
    glPushMatrix()
    glRotated(90, 0, 1, 0)
    glScaled(0.5, 0.5, 5.0)
    glutSolidCube(1)
    glPopMatrix()
    
    # Propellers
    glColor3f(0.0, 0.0, 0.0) 
    propeller_size = 0.1
    # Front-left
    glPushMatrix()
    glTranslated(0, 0.5, 2.5)
    glRotated(90, 1, 0, 0)
    glScaled(propeller_size, propeller_size, propeller_size)
    glutSolidTorus(1, 1, 10, 20)
    glPopMatrix()
    
    # Front-right
    glPushMatrix()
    glTranslated(2.5, 0.5, 0)
    glRotated(90, 1, 0, 0)
    glScaled(propeller_size, propeller_size, propeller_size)
    glutSolidTorus(1, 1, 10, 20)
    glPopMatrix()
    
    # Back-left
    glPushMatrix()
    glTranslated(-2.5, 0.5, 0)
    glRotated(90, 1, 0, 0)
    glScaled(propeller_size, propeller_size, propeller_size)
    glutSolidTorus(1, 1, 10, 20)
    glPopMatrix()
    
    # Back-right
    glPushMatrix()
    glTranslated(0, 0.5, -2.5)
    glRotated(90, 1, 0, 0)
    glScaled(propeller_size, propeller_size, propeller_size)
    glutSolidTorus(1, 1, 10, 20)
    glPopMatrix()
    
    glPopMatrix()
#plane draw and its features
def draw_plane():
    # Main body(blue)
    glColor3f(0.0, 0.0, 1.0) # Blue color
    glPushMatrix()
    # Reduced scale to make the plane smaller
    glScaled(1.5, 0.3, 0.3)
    glutSolidSphere(1.0, 30, 30)
    glPopMatrix()
    
    # Cockpit
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    # Adjusted position - scale for the smaller plane
    glTranslated(0.75, 0.1, 0.0)
    glScaled(0.5, 0.35, 0.4)
    glRotated(20.0, 0, 1, 0)
    glutSolidSphere(0.45, 30, 30)
    glPopMatrix()
    
    # Wings red
    glColor3f(1.0, 0.0, 0.0) # Red color
    glPushMatrix()
    #Adjusted position and scale for the smaller plane
    glTranslated(0.0, 0.0, 1.0)
    glScaled(1.25, 0.1, 0.35)
    glutSolidCube(1.0)
    glPopMatrix()
    glPushMatrix()
    glTranslated(0.0, 0.0, -1.0)
    glScaled(1.25, 0.1, 0.35)
    glutSolidCube(1.0)
    glPopMatrix()
    
    # Engines gula yellowish-brown
    glColor3f(0.8, 0.6, 0.4)
    glPushMatrix()
    glTranslated(0.0, -0.15, 0.9)
    glRotated(90.0, 0, 1, 0)
    glScaled(0.1, 0.1, 0.25)
    glutSolidTorus(0.5, 0.5, 10, 20)
    glPopMatrix()
    glPushMatrix()
    glTranslated(0.0, -0.15, -0.9)
    glRotated(90.0, 0, 1, 0)
    glScaled(0.1, 0.1, 0.25)
    glutSolidTorus(0.5, 0.5, 10, 20)
    glPopMatrix()

    # Tail red
    glColor3f(1.0, 0.0, 0.0) # Red color
    glPushMatrix()
    glTranslated(-1.0, 0.25, 0.0)
    glScaled(0.15, 0.75, 0.15)
    glutSolidCube(1.0)
    glPopMatrix()
#sun draw
def draw_sun():
    # Draw a bright yellow sun high in the sky
    glColor3f(1.0, 1.0, 0.0) # Yellow color
    glPushMatrix()
    glTranslated(70.0, 50.0, -100.0)
    glutSolidSphere(10.0, 30, 30)
    glPopMatrix()
#clouds draw
def draw_cloud(pos_x, pos_y, pos_z, scale):
    
    
    if is_cloud_gray:
    
        glColor4f(0.5, 0.5, 0.5, 0.9)
    else:
    
        glColor4f(1.0, 1.0, 1.0, 0.9)

    glPushMatrix()
    glTranslated(pos_x, pos_y, pos_z)
    glScaled(scale, scale, scale)
    
    
    glPushMatrix()
    glTranslated(0.0, 0.0, 0.0)
    glutSolidSphere(1.0, 20, 20)
    glPopMatrix()
    
    glPushMatrix()
    glTranslated(0.8, -0.2, 0.2)
    glutSolidSphere(0.8, 20, 20)
    glPopMatrix()
    
    glPushMatrix()
    glTranslated(-0.8, 0.2, -0.2)
    glutSolidSphere(0.9, 20, 20)
    glPopMatrix()
    
    glPushMatrix()
    glTranslated(0.5, 0.5, -0.5)
    glutSolidSphere(0.7, 20, 20)
    glPopMatrix()
    
    glPopMatrix()

#scene draw
def draw_scene():
    
    # ground (green)
    glColor3f(0.2, 0.8, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-100.0, 0.0, -100.0)
    glVertex3f( 100.0, 0.0, -100.0)
    glVertex3f( 100.0, 0.0, 100.0)
    glVertex3f(-100.0, 0.0, 100.0)
    glEnd()

    # sob buildings gula
    for b in buildings:
        draw_building(b['x'], b['z'], b['h'], b['w'], b['d'], b['colors'])

    # sob  rings gula loop er vitore
    for r in rings:
        draw_ring(r['x'], r['y'], r['z'], r['rad'], r['thick'])
        
    # drone gulao same vabe
    for d in drones:
     
        draw_drone(d['x'] + d['x_offset'], d['y'], d['z'], d['scale'])

def draw_text(text, x, y):
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT))
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
#ekhane amra play_exist button box draw korbo
def draw_menu_screen():
    
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT))
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    
    # PLAY button r box
    glColor3f(0.2, 0.7, 0.2) # Green color
    glBegin(GL_QUADS)
    glVertex2f(width / 2 - 125, height / 2 - 20)
    glVertex2f(width / 2 + 5, height / 2 - 20)
    glVertex2f(width / 2 + 5, height / 2 + 20)
    glVertex2f(width / 2 - 125, height / 2 + 20)
    glEnd()
    glColor3f(1.0, 1.0, 1.0) 
    draw_text("PLAY", width / 2 - 85, height / 2 - 5)

    # EXIT button r box ekhane amra gl quads use korsi
    glColor3f(0.8, 0.2, 0.2) 
    glBegin(GL_QUADS)

    glVertex2f(width / 2 + 25, height / 2 - 20)
    glVertex2f(width / 2 + 95, height / 2 - 20)
    glVertex2f(width / 2 + 95, height / 2 + 20)
    glVertex2f(width / 2 + 25, height / 2 + 20)
    glEnd()
    glColor3f(1.0, 1.0, 1.0) 
    draw_text("EXIT", width / 2 + 45, height / 2 - 5)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
#game over screen er moddhe je game over and final score box asbe ta draw kora
#ekhane jodi new high score load hoi tahole sei high score ta chng hbe
#ar egula draw korar jonno mainly ami glquads use korsi
def draw_game_over_screen():

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT))
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)


    glColor3f(0.0, 0.0, 0.0)
    draw_text("GAME OVER!", width / 2 - 80, height / 2 + 60)
    draw_text(f"Final Score: {score}", width / 2 - 80, height / 2 + 30)
    
 
    if is_new_high_score:
        draw_text("NEW HIGH SCORE!", width / 2 - 80, height / 2)

    # Play Again button & box
    glColor3f(0.2, 0.7, 0.2) # Green color
    glBegin(GL_QUADS)

    glVertex2f(width / 2 - 145, height / 2 - 50)
    glVertex2f(width / 2 + 5, height / 2 - 50)
    glVertex2f(width / 2 + 5, height / 2 - 10)
    glVertex2f(width / 2 - 145, height / 2 - 10)
    glEnd()
    glColor3f(1.0, 1.0, 1.0) 
    draw_text("PLAY AGAIN", width / 2 - 115, height / 2 - 35)

    # Exit button r box
    glColor3f(0.8, 0.2, 0.2) 
    glBegin(GL_QUADS)
    
    glVertex2f(width / 2 + 25, height / 2 - 50)
    glVertex2f(width / 2 + 95, height / 2 - 50)
    glVertex2f(width / 2 + 95, height / 2 - 10)
    glVertex2f(width / 2 + 25, height / 2 - 10)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    draw_text("EXIT", width / 2 + 45, height / 2 - 35)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
#live feature tao edike include
#endless runner
def idle():
    
    global pln_po_z, score, is_gam_over_, buildings, rings, clouds, drones, high_score, is_new_high_score, lives, pln_po_x, pln_po_y, pln_rota_x, pln_rota_y, pln_rota_z, is_gam_strt_, intro_scren, countdown_timer, plane_speed
    
    if is_gam_strt_ and not is_gam_over_:
      #score 150 er beshi hole speed barbe  
        if score >= 150:
            plane_speed = 2
        
        #endless e cholar jonno loop er moddhe diye dibo
        
        for b in buildings: #endless buildings
            b['z'] += plane_speed
        for r in rings: #endless rings
            r['z'] += plane_speed
        for c in clouds: #endless clouds
            c['z'] += plane_speed * 0.5 
        for d in drones: #endless drones
            d['z'] += plane_speed
           
            if d['x_offset'] > 15:
                d['direction'] = -1
            elif d['x_offset'] < -15:
                d['direction'] = 1
        
            d['x_offset'] += d['direction'] * 0.1

        #building er collison er oart ta
        if pln_po_y < 0.5: # y axis 0.5 er beshi move korle then collison hbe lives harabe 
            #jotokhn lives cholte thake tototkhn
            #lives sesh hoye gele else er vitore dhuke
            if lives > 1:
                lives -= 1
                pln_po_x = 0.0
                pln_po_y = 5.0
                print(f"Hard landing! You have {lives} lives remaining.")
           
            else:
                is_gam_over_ = True
                if score > high_score:
                    high_score = score
                    is_new_high_score = True
                    save_high_score(high_score)
                print("GAME OVER! Your plane has crashed on the ground.")

        
        new_buildings = []
        for b in buildings:
        
            if (abs(pln_po_x - b['x']) < b['w'] / 2 + 1.5 and
                abs(pln_po_y - b['h'] / 2) < b['h'] / 2 + 0.2 and
                abs(pln_po_z - b['z']) < b['d'] / 2 + 1.5):
            
                if lives > 1:
                    lives -= 1
                    print(f"Collision! You have {lives} lives remaining.")
                
                    pln_po_x = 0.0
                    pln_po_y = 5.0
                else:
                    is_gam_over_ = True
                
                    if score > high_score:
                        high_score = score
                        is_new_high_score = True
                        save_high_score(high_score) 
                    print("GAME OVER! The plane has crashed into a building.")
            
        
            if b['z'] < 50:
                new_buildings.append(b)

        buildings.clear()
        buildings.extend(new_buildings)
        
        #then tkhn jotogula rings er vitore dhukhse totogular point count hbe
        new_rings = []
        for r in rings:
        
            if abs(pln_po_z - r['z']) < 1.0:
            
                dist = (pln_po_x - r['x'])**2 + (pln_po_y - r['y'])**2
                if dist < (r['rad'] - r['thick'] / 2)**2:
                    score += 10
                    print(f"Ring collected! Score: {score}")
            
            
            if r['z'] < 50:
                new_rings.append(r)
        
        rings.clear()
        rings.extend(new_rings)

        
        new_clouds = []
        for c in clouds:
            if c['z'] < 50:
                new_clouds.append(c)
        clouds.clear()
        clouds.extend(new_clouds)
        
        
        new_drones = []
        for d in drones:
        
            if (abs(pln_po_x - (d['x'] + d['x_offset'])) < 1.5 and
                abs(pln_po_y - d['y']) < 1.5 and
                abs(pln_po_z - d['z']) < 1.5):
            
                if lives > 1:
                    lives -= 1
                    print(f"Collision! You have {lives} lives remaining.")
                
                    pln_po_x = 0.0
                    pln_po_y = 5.0
                else:
                    is_gam_over_ = True
                    if score > high_score:
                        high_score = score
                        is_new_high_score = True
                        save_high_score(high_score) 
                    print("GAME OVER! You were hit by a drone.")
            
            if d['z'] < 50:
                new_drones.append(d)
        drones.clear()
        drones.extend(new_drones)
        
       
        if len(buildings) < 30 or len(rings) < 3:
            generate_obstacles()

    glutPostRedisplay()

# GLUT Callbacks
#Anika

#Camera Mode
def display():
    global intro_scren, is_gam_strt_, countdown_timer, camera_mode, came_posi_x, came_posi_y, came_posi_z, pln_po_x, pln_po_y, pln_po_z, is_gam_over_

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    if intro_scren:
        draw_menu_screen()
    elif is_gam_over_:
        draw_game_over_screen()
    else:

        if camera_mode == 'first_person':
            gluLookAt(pln_po_x, pln_po_y, pln_po_z + 5.0,
                      pln_po_x, pln_po_y, pln_po_z,
                      0, 1, 0)
        
        elif camera_mode == 'second_person':
            gluLookAt(pln_po_x, pln_po_y + 1.0, pln_po_z - 5.0,
                      pln_po_x, pln_po_y, pln_po_z,
                      0, 1, 0)

        elif camera_mode == 'third_person':
            gluLookAt(came_posi_x, came_posi_y, came_posi_z,
                      pln_po_x, pln_po_y, pln_po_z,
                      0, 1, 0)

        
        glPushMatrix()
        glTranslated(pln_po_x, pln_po_y, pln_po_z)
        glRotated(pln_rota_x, 1, 0, 0)
        glRotated(pln_rota_y, 0, 1, 0)
        glRotated(pln_rota_z, 0, 0, 1)
        draw_plane()
        glPopMatrix()
        
        
        if is_sun_visible:
            draw_sun()

        
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for c in clouds:
            draw_cloud(c['x'], c['y'], c['z'], c['scale'])
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

        
        glPushMatrix()
        glTranslated(0, 0, 0)
        draw_scene()
        glPopMatrix()
        
        
        draw_text(f"Score: {score}", 20, glutGet(GLUT_WINDOW_HEIGHT) - 30)
        draw_text(f"Lives: {lives}", 20, glutGet(GLUT_WINDOW_HEIGHT) - 60)
        draw_text(f"High Score: {high_score}", 20, glutGet(GLUT_WINDOW_HEIGHT) - 90)
        draw_text(f"Camera: {camera_mode.replace('_', ' ').title()}", 20, glutGet(GLUT_WINDOW_HEIGHT) - 120)
        
#countdown feature edike    
        if countdown_timer >= 0:
            if countdown_timer > 0:
                text = f"GET READY {countdown_timer}"
            else:
                text = "GO!"
            draw_text(text, glutGet(GLUT_WINDOW_WIDTH) / 2 - 80, glutGet(GLUT_WINDOW_HEIGHT) / 2)


    glutSwapBuffers()

def reshape(width, height):
    
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, width / height, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
#rotation r keyboard handle er part gula
def keyboardListener(key, x, y):
    
    global intro_scren, pln_rota_z, is_gam_strt_, is_gam_over_, camera_mode, came_posi_x, came_posi_y, is_cloud_gray, is_sun_visible
    

    if intro_scren or is_gam_over_:
        return

    key = key.decode("utf-8").lower()

#keyboard r camera mode gula handle kore edike    
    if camera_mode == 'third_person':
        
        if key == 'a':
            came_posi_y += 1
        
        elif key == 's':
            came_posi_y -= 1
        
        elif key == 'w':
            came_posi_x -= 1
        
        elif key == 'e':
            came_posi_x += 1
            
    # Roll counter-clockwise (Z key)
    if key == 'z':
        pln_rota_z += 2
    # Roll clockwise (X key)
    elif key == 'x':
        pln_rota_z -= 2
    # Start/Pause game
    elif key == ' ':
        if not is_gam_over_:
            is_gam_strt_ = not is_gam_strt_
    # Reset game
    elif key == 'r':
        reset_game()
    # Camera view
    elif key == '1':
        camera_mode = 'first_person'
    elif key == '2':
        camera_mode = 'second_person'
    elif key == '3':
        camera_mode = 'third_person'
    # Toggle gray clouds
    elif key == '4':
        is_cloud_gray = not is_cloud_gray
    # sun visibility
    elif key == '5':
        is_sun_visible = not is_sun_visible


    glutPostRedisplay()
#arrow key gular movement gula fix kore mane plane kothay kototuk move korbe hen ten
def specialKeyListener(key, x, y):
    
    global pln_po_x, pln_po_y
    
    
    if intro_scren or is_gam_over_:
        return

    # plane up mane upore
    if key == GLUT_KEY_UP:
        pln_po_y += plane_speed * 2
    # plane nicher dike
    if key == GLUT_KEY_DOWN:
        pln_po_y -= plane_speed * 2
    # plane bame
    if key == GLUT_KEY_LEFT:
        pln_po_x -= plane_speed * 2
    # plane dane
    if key == GLUT_KEY_RIGHT:
        pln_po_x += plane_speed * 2
    
    glutPostRedisplay()
#countdown func ke arekbar call korar jonno
def countdown_timer_callback(value):
    
    global countdown_timer, is_gam_strt_
    
    if countdown_timer > 0:
        countdown_timer -= 1
        glutTimerFunc(1000, countdown_timer_callback, 0) 
    else:
        is_gam_strt_ = True 
        countdown_timer = -1 

    glutPostRedisplay()
#mouse diye play pause je handle kore
def mouseListener(button, state, x, y):
    
    global intro_scren, is_gam_strt_, countdown_timer, is_gam_over_
    width = glutGet(GLUT_WINDOW_WIDTH)
    height = glutGet(GLUT_WINDOW_HEIGHT)
    
    inverted_y = height - y

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if intro_scren:
        
            if (x >= width / 2 - 125 and x <= width / 2 + 5 and
                inverted_y >= height / 2 - 20 and inverted_y <= height / 2 + 20):
                intro_scren = False
                countdown_timer = 5 
                glutTimerFunc(1000, countdown_timer_callback, 0) 
                print("Starting countdown...")
                glutPostRedisplay()
            
            
            elif (x >= width / 2 + 25 and x <= width / 2 + 95 and
                  inverted_y >= height / 2 - 20 and inverted_y <= height / 2 + 20):
                print("Exiting game.")
                glutLeaveMainLoop()
        
        elif is_gam_over_:
            
            if (x >= width / 2 - 145 and x <= width / 2 + 5 and
                inverted_y >= height / 2 - 50 and inverted_y <= height / 2 - 10):
                reset_game()
                intro_scren = False 
                countdown_timer = 5
                glutTimerFunc(1000, countdown_timer_callback, 0)
                print("Starting new game countdown...")
                glutPostRedisplay()
            
            
            elif (x >= width / 2 + 25 and x <= width / 2 + 95 and
                  inverted_y >= height / 2 - 50 and inverted_y <= height / 2 - 10):
                print("Exiting game.")
                glutLeaveMainLoop()
#MUMU
#Drone
#drone jegula genrate chilo ta ekhane call kore
def generate_obstacles():
    
    global buildings, rings, clouds, drones, score
    
    
    colors = [
        (0.8, 0.4, 0.6), 
        (0.4, 0.6, 0.8), 
        (0.6, 0.8, 0.4), 
        (0.8, 0.6, 0.4), 
        (0.5, 0.5, 0.5), 
        (0.4, 0.8, 0.6), 
        (0.7, 0.3, 0.9), 
        (0.9, 0.7, 0.1) 
    ]

#je kono side theke e drone asha shuru kore    
    for _ in range(15):
        
        side = random.choice(['left', 'right'])
        
        if side == 'left':
            x = random.uniform(-40, -20)
        else:
            x = random.uniform(20, 40)
            
        
        z = random.uniform(-250, -150)
        h = random.uniform(20, 50)
        w = random.uniform(5, 10)
        d = random.uniform(5, 10)
        
        
        segment_height = 2.0
        num_segments = int(h / segment_height)
        segment_colors = [random.choice(colors) for _ in range(num_segments)]

        buildings.append({'x': x, 'z': z, 'h': h, 'w': w, 'd': d, 'colors': segment_colors})
        
    
    for _ in range(1):
        x = random.uniform(-20, 20)
        y = random.uniform(5, 15)
        
        z = random.uniform(-250, -150)
        rad = 5.0
        thick = 1.0
        rings.append({'x': x, 'y': y, 'z': z, 'rad': rad, 'thick': thick})

    
    for _ in range(3):
        x = random.uniform(-50, 50)
        y = random.uniform(20, 40)
        z = random.uniform(-500, -250)
        scale = random.uniform(5, 10)
        clouds.append({'x': x, 'y': y, 'z': z, 'scale': scale})
    
#score jkhn 100 hoi tkhn drone appear kora shuru kore  
    if score >= 100:
        if len(drones) < 2:
            x = random.uniform(-15, 15)
            y = random.uniform(10, 20)
            z = random.uniform(-250, -150)
            scale = 2.0
            drones.append({'x': x, 'y': y, 'z': z, 'scale': scale, 'x_offset': 0, 'direction': 1})
            print("New drone added!")

#game reset korar jonno
def reset_game():
    
    global pln_po_x, pln_po_y, pln_rota_x, pln_rota_y, pln_rota_z, is_gam_strt_, is_gam_over_, score, buildings, rings, clouds, drones, intro_scren, countdown_timer, is_new_high_score, lives, plane_speed, is_sun_visible, is_cloud_gray
    
    pln_po_x, pln_po_y = 0.0, 5.0
    pln_rota_x, pln_rota_y, pln_rota_z = 0.0, 0.0, 0.0
    intro_scren = True
    is_gam_strt_ = False
    is_gam_over_ = False
    score = 0
    lives = 3 
    buildings = []
    rings = []
    clouds = []
    drones = []
    countdown_timer = -1 
    is_new_high_score = False 
    plane_speed = 1 
    is_sun_visible = False 
    is_cloud_gray = False 
    
    generate_obstacles()
    print("Game reset")
#high score load er jonno
def load_high_score():
    
    global high_score
    try:
        
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_score.txt")
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                high_score = int(f.read())
                print(f"High score loaded: {high_score}")
        else:
            
            with open(file_path, "w") as f:
                f.write("0")
            high_score = 0
            print("High score file not found, created a new one with a score of 0.")
    except (IOError, ValueError) as e:
        high_score = 0
        print(f"Error loading high score: {e}. Starting with high score 0.")
#high score save koreee
def save_high_score(score_to_save):
    
    try:
        
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_score.txt")
        with open(file_path, "w") as f:
            f.write(str(score_to_save))
            print(f"High score saved: {score_to_save}")
    except IOError as e:
        print(f"Error saving high score: {e}.")
#main func gula call kore 
def main():
    
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Plane Game".encode('ascii'))
    
    
    glClearColor(0.5, 0.8, 1.0, 1.0) 
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)

    
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    
   
    glutSpecialFunc(specialKeyListener)
    glutKeyboardFunc(keyboardListener)
    glutMouseFunc(mouseListener)

    
    glutMainLoop()
    

if __name__ == '__main__':
    load_high_score()
    main()