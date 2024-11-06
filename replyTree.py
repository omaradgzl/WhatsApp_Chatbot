class TreeNodes:
    """
    Class created for answering system. It allows contacts to control a system such as a menu.
    """
    
    def __init__(self, name = None, info = None, childrens = None , order = None):
        self.name = name
        self.info = info
        self.childrens = childrens
        self.order = order
    
    def selectChildren(self,index):
        """
        Selects children menu.

        Parameters
        ----------
        index : int
            Selected menu number.

        Returns
        -------
        TreeNodes
            Selected menu object.

        """
        try:
            return self.childrens[index-1]
        except:
            return self
        
    def getInfo(self):
        """
        Gets answer.

        Returns
        -------
        str
            String to answer.

        """
        try:
            return self.name + " \n" +  self.info
        except Exception as e:
            print(str(e))
    
    def setParent(self,parent):
        """
        Sets parent menu.

        Parameters
        ----------
        parent : TreeNodes
            Parent menu object.

        Returns
        -------
        None.

        """
        self.parent = parent
    
    def getParent(self):
        """
        Gets parent menu

        Returns
        -------
        TreeNode
            Parent menu object.

        """
        try:
            return self.parent
        except:
            return self
    
            
def createMenus():
   
     """
     Creates menus.
    
     Returns
     -------
     TreeNode
        Main menu object.
    
     """
     menuA = TreeNodes("","Değerli Çalışanımız, TextTextText",order=-1)
     menuB = TreeNodes("","Değerli Çalışanımız, TextTextText" ,order=-1)
     menuC = TreeNodes("","Değerli Çalışanımız, TextTextText",order=-1)
     menuD = TreeNodes("","Değerli Çalışanımız, TextTextText",order=-1)
     menuE = TreeNodes("","Değerli Çalışanımız, TextTextText",order=-1)
     menuF = TreeNodes("","Değerli Çalışanımız, TextTextText",order=-1)
     menuG = TreeNodes("","Değerli Çalışanımız, TextTextText",order=-1)
     menuH = TreeNodes("","Değerli Çalışanımız, TextTextText",order=-1)
     menuI = TreeNodes("","Değerli Çalışanımız, TextTextText",order=-1)
     
    
     defaultText = '''
     İhtiyaç duyduğunuz her anda iş  süreçlerinde size rehberlik etmek için yanınızdayız. 
     Kişisel bilgisayarlarınızdan İntranet sayfamız olan  
     hebelehübelehebelehübeleopalagopala
     adresinden şirketimizle ilgili tüm duyuru ve haberlere,  faydalı linklere , iç ilanlara erişebilirsiniz.
     '''
     
     menuText = '''
     Size buradan bir çok konu ile ilgili yardımcı olabilirim. 
     Lütfen size yardımcı olmamı istediğiniz konu numarasını yazarak mesajı cevaplayınız.
     İşlemleri sonlandırmak için "-1" , tekrar bu menüye dönmek için "0" yazınız.
    
    1) Menu - 1
    2) Menu - 2
    3) Menu - 3
    4) Menu - 4
    5) Menu - 5 
    6) Menu - 6 
    7) Menu - 7
    8) Menu - 8
    9) Menu - 9 
     '''
    
     mainMenu = TreeNodes(defaultText,menuText,[menuA,menuB,menuC,menuD,menuE,menuF,menuG,menuH,menuI],0)
     
     
     menuA.setParent(mainMenu)
     menuB.setParent(mainMenu)
     menuC.setParent(mainMenu)
     menuD.setParent(mainMenu)
     menuE.setParent(mainMenu)
     menuF.setParent(mainMenu)
     menuG.setParent(mainMenu)
     menuH.setParent(mainMenu)
     menuI.setParent(mainMenu)
     
     
     return mainMenu







