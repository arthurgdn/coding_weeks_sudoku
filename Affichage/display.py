from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from functools import partial
from Reconnaissance.photo_to_grid import *
from Resolution.résolution import *
from Resolution.resolution_optimisée import *
from Generation.generation import *
from Affichage.display_hidato import *
import numpy as np
from PIL import Image, ImageTk





def main_window():
    """On défini la fenêtre principale"""
    root = Tk()
    root.configure(background = "white")
    root.title("Résolution de Sudoku")    
    root.resizable(0,0)
    root.geometry('500x500')
    button_frame=Frame(root)
    button_frame.configure(background = "white")
    Grid.columnconfigure(root,0,weight=1)
    scan_button = Button(button_frame,text="Scanner une grille", bg = "black", fg = "snow",command=partial(choix_model,root))
    scan_button.textcolor = "snow"
    load = Image.open("titre.jpg").resize((500,120))
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.image = render
    img.place(x = 0, y = 0)


    """Transforme la grille pour la renvoyer au bon format"""
    def transform(grille):
        print(grille)
        for i in range(9):
            for j in range(9):
                
                if grille[i][j] == 0.0:
                    grille[i][j] = ''
                else: grille[i][j] = int(grille[i][j])
        return grille
    """Popup avec une interface pour choisir la difficulté de la grille """
    def generate():
        popup = Tk()
        def destroy():
            diff = choix_difficulte.curselection()
            diff = choix_difficulte.get(diff)
            p_bar = loading_bar(popup,diff)
            saisir_grille(root,transform(generation(diff, p_bar).tolist()))
            popup.destroy()
            

        popup.wm_title("Générer grille")
        label = Label(popup, text="Veuillez séléctionner la difficulté de la grille")
        label.pack(side="top", fill="x", pady=10)
        radio_frame = Frame(popup)

        choix_difficulte = Listbox(radio_frame,selectmode=SINGLE,width=50)
        choix_difficulte.insert(1,"Facile")
        choix_difficulte.insert(2,"Moyen")
        choix_difficulte.insert(3,"Difficile")
        choix_difficulte.selection_set(first=0)
        choix_difficulte.grid(sticky=N+S+E+W)

        radio_frame.pack(fill="x",pady=10)
        B1 = Button(popup, text="Générer", command = destroy)
        B1.pack(side="bottom")
        popup.mainloop()
        return None
    game_grid = []
    for i in range(9):
        game_grid.append([])
        for j in range(9):
            game_grid[i].append('')
    saisir_button = Button(button_frame,bg = "black", fg = "white",text="Saisir la grille",command=partial(saisir_grille,root,game_grid))
    generer_button = Button(button_frame,bg = "black", fg = "white",text="Générer la grille",command=generate)
    hidato_button = Button(button_frame,bg = "#8B2230",text="Hidato",command=partial(saisir_grille_hidato,root),width=14)
    quit_button = Button(root,text="Quitter", bg = "black", fg = "snow",command=quit)
    saisir_button.grid(row=2,column=0,ipady=15,padx=15)
    scan_button.grid(row=2,column=1,ipady=15,pady=30,padx=15)
    generer_button.grid(row=2,column=2,ipady=15,pady=30,padx=15)
    hidato_button.grid(row=3,column=1,ipady = 15, padx=15)
    button_frame.grid(row=2,column=0)
    quit_button.grid(row=4,column=0)
    Grid.rowconfigure(root,0,weight=1)
    Grid.rowconfigure(root,1,weight=1)
    Grid.rowconfigure(root,2,weight=1)
    Grid.rowconfigure(root,3,weight=1)
    Grid.columnconfigure(button_frame,0,weight=1)
    Grid.columnconfigure(button_frame,2,weight=1)
    Grid.columnconfigure(button_frame,1,weight=1)
    root.mainloop()

def loading_bar(window,maxValue):
    progressbar=ttk.Progressbar(window,orient="horizontal",length=300,mode="determinate")
    progressbar.pack(side=BOTTOM)
    currentValue=0
    progressbar["value"]=0
    return progressbar




def open_scan(root,model):
    """On ouvre une fenetre pour choisir l'image à scanner"""
    filename = filedialog.askopenfilename(initialdir = "/images",title = "Selectionnez une image",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    grid = photo_to_grid(filename,model)
    popupmsg(root,grid)

def popupmsg(root,grid):
    """
    Ouvre un popup pour dire à l'utilisateur de vérifier la grille scannée
    """
    popup = Tk()
    def destroy():
        popup.destroy()
        saisir_grille(root,grid)
    popup.wm_title("Verifier la grille")
    label = Label(popup, text="Veuillez verifier que la grille a bien été remplie et corriger les erreurs")
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = destroy)
    B1.pack()
    popup.mainloop()

def choix_model(root):
    """On demande à l'utilisateur si la grille est remplie à la main ou à l'ordie"""
    popup = Tk()
    choix = StringVar(popup)
    choix.set('main')
    main = Radiobutton(popup, text='main', value='main', variable=choix)
    ordi = Radiobutton(popup, text='ordinateur', value='ordi', variable=choix)
    
    main.grid(row=1, column=0, sticky='W') 
    ordi.grid(row=1, column=2, sticky='W')

    def destroy():
        popup.destroy()
        open_scan(root,choix.get())
        
        
        
    popup.wm_title("Choix du modèle")
    label = Label(popup, text="La grille de sudoku est-elle écrite à la main ou par ordinateur ?")
    label.grid(row = 0, column = 1)
    B1 = Button(popup, text="Valider", command = destroy)
    B1.grid(row = 2, column = 1)
    popup.mainloop()

def affiche_grille(root,grille):
    """Interface pour afficher la grille"""
    grid = Toplevel(root)
    grid.title("Sudoku")
    """On divise la grille en sous grille pour afficher les 9 sous carrés avec un bord plus épais"""
    main_grid = []
    for i in range(3):
        ligne = []
        for j in range(3):
            f = Frame(grid, bd=2, relief='solid', height =300, width = 300)
            ligne.append(f)
        main_grid.append(ligne)
    for i in range(3):
        for j in range(3):
            main_grid[i][j].grid(row=i, column = j, sticky=N+S+E+W)      
    

    for x in range(3):
        Grid.columnconfigure(grid, x, weight=1)

    for y in range(3):
        Grid.rowconfigure(grid, y, weight=1)    
    
    graphical_grid=[]
    for i in range(9):
        ligne = []
        for j in range(9):
            f = Frame(main_grid[i//3][j//3],bg="white", bd=1, relief='solid', height =100, width = 100)
            ligne.append((f,Label(f,font="Arial 20",justify="center",bg="white",bd=0,text=grille[i][j])))
            ligne[j][1].pack(expand = YES)
        graphical_grid.append(ligne)
    for i in range(9):
        for j in range(9):
            graphical_grid[i][j][0].grid(row=i%3, column = j%3, sticky=N+S+E+W) 

    for x in range(3):
        for i in range(3):
            for j in range(3):
                Grid.columnconfigure(main_grid[i][j], x, weight=1)
                Grid.rowconfigure(main_grid[i][j],x,weight=1)

    grid.grid()
def check_grid(root,grille,grille_initiale):
    """Verifie si la grille qui est envoyé est correcte """
    def transform_grille():
        """Transforme la grille pour la mettre au bon format"""
        grille_intermediaire = []
        for i in range(9):
            grille_intermediaire.append([])
            for j in range(9):
                grille_intermediaire[i].append(grille[i][j])
        for i in range(9):
            for j in range(9):
                if grille_intermediaire[i][j] == 0:
                    grille_intermediaire[i][j] = ''
                elif type(grille_intermediaire[i][j]) == int:
                    grille_intermediaire[i][j] = [grille_intermediaire[i][j]]
        return grille_intermediaire
        
    correcte = verification_grille(transform_grille())
    def popupcheck(correcte):
        """Popup qui affiche si la grille est correcte"""
        popup = Tk()
        def destroy():
            popup.destroy()
            if correcte:
                root.destroy
        if correcte:
            popup.wm_title("Sudoku")
            label = Label(popup, text="La grille est correcte vous avez gagné!")
        else:
            popup.wm_title("Sudoku")
            label = Label(popup, text="La grille est incorrecte, veuillez rééssayer")
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command = destroy)
        B1.pack()
        popup.mainloop()
    popupcheck(correcte)
    


    
def play_grid(root,grille,grille_modif):

    def grid_to_list():
        """Recupere les entrees pour les mettre sous forme de liste"""
        sudoku_grid = []
        for i in range(9):
            sudoku_grid.append([])
            for j in range(9):
                if type(graphical_grid[i][j][1]) == Entry:
                    value = graphical_grid[i][j][1].get()
                elif type(graphical_grid[i][j][1])==Label:
                    value = graphical_grid[i][j][1].cget("text")
                if value=='':
                    sudoku_grid[i].append('')
                else: sudoku_grid[i].append(int(value))
        check_grid(root,sudoku_grid,grille)
    def suggest():
        def update_transform_grid():
            """recupere les valeurs de la grille et les mets au bon format"""
            sudoku_grid = []
            for i in range(9):
                sudoku_grid.append([])
                for j in range(9):
                    if type(graphical_grid[i][j][1]) == Entry:
                        value = graphical_grid[i][j][1].get()
                    elif type(graphical_grid[i][j][1])==Label:
                        value = graphical_grid[i][j][1].cget("text")
                    if value=='':
                        sudoku_grid[i].append('')
                    else: sudoku_grid[i].append([int(value)])
            return sudoku_grid
            
        """Interface pour donner un indice à l'utilisateur"""
        indice = donner_indice(update_transform_grid())
        popup = Tk()
        def destroy():
            popup.destroy()
        if indice==False:
            popup.wm_title("Sudoku - Indice")
            label = Label(popup, text="Nous ne pouvons pas vous donner d'indice sur cette grille !")
        else:
            popup.wm_title("Sudoku - Indice")
            label = Label(popup, text="Un " + str(indice[1]) + " va être rempli en case "+ str(indice[0][0] + 1) + ","+str(indice[0][1]+1))
            i,j = indice[0][0],indice[0][1]
            graphical_grid[i][j][1].insert(0,indice[1])
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Okay", command = destroy)
        B1.pack()
        popup.mainloop()
    def sup():
        """Permet à l'utilisateur d'ajouter des suppositions à la case selectionnée"""
        for k in range(9):
            for l in range(9):
                if graphical_grid[k][l][1] == window.focus_get():
                    i,j = k,l
        pop = Tk()
        def destroy():
            
            current_suppo = graphical_grid[i][j][2].cget("text")
            suppo = current_suppo + " " + str(entre_supposition.get())
            print(suppo)
            graphical_grid[i][j][2].config(text=suppo)
            pop.destroy()
        pop.wm_title("Sudoku - Supposition")
        
        label = Label(pop, text="Vous pouvez faire une supposition pour la case selectionnée :")
        label.pack(side="top", fill="x", pady=10)
        entre_supposition = Entry(pop)
        entre_supposition.pack()
        B1 = Button(pop, text="Okay", command = destroy)
        B1.pack()
        pop.mainloop()
        
        

    """Affiche l'interface pour jouer avec des boutons pour donner une suggestion ou ajouter une supposition"""
    window = Toplevel(root)
    window.title("Sudoku")
    window.resizable(0,0)
    window.grid()
    grid = Frame(window)
    
    frame_tools = Frame(window)
    suggestion_button=Button(frame_tools,text="Suggestion",command=suggest)
    supposition_button=Button(frame_tools,text="Insérer une supposition",command=sup)
    suggestion_button.grid(row=0,column=0,padx = 15,ipady = 5,pady=5)
    supposition_button.grid(row=0,column=1,padx= 15,ipady=5,pady=5)
    frame_button = Frame(window)
    check_button = Button(frame_button,text="Vérifier",command=grid_to_list)
    check_button.grid(row=0,column=0,sticky=N+S+E+W)
    Grid.columnconfigure(frame_button,0,weight=1)
    Grid.rowconfigure(frame_button,0,weight=1)
    main_grid = []
    for i in range(3):
        ligne = []
        for j in range(3):
            f = Frame(grid, bd=2, relief='solid', height =300, width = 300)
            ligne.append(f)
        main_grid.append(ligne)

    


    for i in range(3):
        for j in range(3):
            main_grid[i][j].grid(row=i, column = j, sticky=N+S+E+W)      
    

    for x in range(3):
        Grid.columnconfigure(grid, x, weight=1)

    for y in range(3):
        Grid.rowconfigure(grid, y, weight=1)    
    
    graphical_grid=[]
    for i in range(9):
        ligne = []
        for j in range(9):
            f = Frame(main_grid[i//3][j//3],bg="white", bd=1, relief='solid', height =100, width = 100)
            supposition = Label(f,font="Arial 10",justify="center",bg="white",bd=0,width=5,text="")
            if grille[i][j] != '':
                ligne.append((f,Label(f,font="Arial 20",justify="center",bg="white",bd=0,text=grille[i][j],width=5),supposition))
            elif grille_modif[i][j] != '':
                e = Entry(f,font="Arial 20",justify="center",bd=0,width=5)
                e.insert(0,grille_modif[i][j])
                ligne.append((f,e,supposition))
            else:
                e = Entry(f,font="Arial 20",justify="center",bd=0,width=5)
                ligne.append((f,e,supposition))
            ligne[j][2].pack()
            ligne[j][1].pack(expand=YES)
            
        graphical_grid.append(ligne)
    for i in range(9):
        for j in range(9):
            graphical_grid[i][j][0].grid(row=i%3, column = j%3, sticky=N+S+E+W) 

    for x in range(3):
        for i in range(3):
            for j in range(3):
                Grid.columnconfigure(main_grid[i][j], x, weight=1)
                Grid.rowconfigure(main_grid[i][j],x,weight=1)
    frame_tools.grid(row=0,column=0,sticky=N+S+E+W)
    grid.grid(row=1,column=0,sticky=N+S+E+W)
    frame_button.grid(row=2,column=0,sticky=N+S+E+W)
    Grid.rowconfigure(window,1,weight=1)
    Grid.columnconfigure(window,0,weight=1)
    


def saisir_grille(root,grille):
    """Interface pour saisir la grille et pour la vérifier après l'avoir scannée"""
    def grid_to_list(action):
        sudoku_grid = []
        for i in range(9):
            sudoku_grid.append([])
            for j in range(9):
                value = graphical_grid[i][j][1].get()
                if value=='':
                    sudoku_grid[i].append('')
                else: sudoku_grid[i].append(int(value))
        if action == 'solve':
            print(sudoku_grid)
            affiche_grille(root,resolve(transform_grid(sudoku_grid)))
            window.destroy()
        elif action =='play':
            grille_modif = []
            for i in range(9):
                grille_modif.append([])
                for j in range(9):
                    grille_modif[i].append('')
            play_grid(root,sudoku_grid,grille_modif)
            window.destroy()
    window = Toplevel(root)
    window.title("Saisir une grille de Sudoku")
    window.grid()
    grid = Frame(window)
    frame_button = Frame(window)
    play_button = Button(frame_button,text="Jouer",command=partial(grid_to_list,'play'))
    solve_button = Button(frame_button,text="Résoudre",command=partial(grid_to_list,'solve'))
    play_button.grid(row=0,column=0,sticky=N+S+E+W)
    solve_button.grid(row=0,column=1,sticky=N+S+E+W)
    Grid.columnconfigure(frame_button,0,weight=1)
    Grid.columnconfigure(frame_button,1,weight=1)
    Grid.rowconfigure(frame_button,0,weight=1)
    main_grid = []
    for i in range(3):
        ligne = []
        for j in range(3):
            f = Frame(grid, bd=2, relief='solid', height =300, width = 300)
            ligne.append(f)
        main_grid.append(ligne)

    


    for i in range(3):
        for j in range(3):
            main_grid[i][j].grid(row=i, column = j, sticky=N+S+E+W)      
    

    for x in range(3):
        Grid.columnconfigure(grid, x, weight=1)

    for y in range(3):
        Grid.rowconfigure(grid, y, weight=1)    
    
    graphical_grid=[]
    for i in range(9):
        ligne = []
        for j in range(9):
            f = Frame(main_grid[i//3][j//3],bg="white", bd=1, relief='solid', height =100, width = 100)
            e = Entry(f,font="Arial 20",justify="center",bd=0)
            e.insert(0,str(grille[i][j]))
            ligne.append((f,e))
            ligne[j][1].pack(expand = YES)
        graphical_grid.append(ligne)
    for i in range(9):
        for j in range(9):
            graphical_grid[i][j][0].grid(row=i%3, column = j%3, sticky=N+S+E+W) 

    for x in range(3):
        for i in range(3):
            for j in range(3):
                Grid.columnconfigure(main_grid[i][j], x, weight=1)
                Grid.rowconfigure(main_grid[i][j],x,weight=1)

    grid.grid(row=0,column=0,sticky=N+S+E+W)
    frame_button.grid(row=1,column=0,sticky=N+S+E+W)
    Grid.rowconfigure(window,0,weight=1)
    Grid.columnconfigure(window,0,weight=1)
    
