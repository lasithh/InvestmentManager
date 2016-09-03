from django.utils.html_parser import HTMLParser


class MarketIndicesHTMLParser(HTMLParser):
    divClass = ('class', 'inner_grid')
    
    isInsideDiv = False
    isInsideTable = False
    
    rowsToIgnore = [0, 1, 2, 5]
    cellsToIgnore = []
    
    readCurrentRow = False;
    readCurrentCell = False;
    
    currentRow = 0
    currentCell = 0
    
    
    extractedData = []
    extractedDataOfCurrentRow = []
    currentData = []
    
    def handle_starttag(self, tag, attrs):
        
        
        #Set the context of HTML Doc
        if self.isInsideDiv and tag == 'table':
            self.isInsideTable = True
        
        if tag == 'div' and self.divClass in attrs:
            self.isInsideDiv = True
        
        if self.isInsideTable and tag == 'tr':
            if self.currentRow not in self.rowsToIgnore:
                self.readCurrentRow = True
                self.currentCell = 0
            
                
        
        if self.readCurrentRow and tag == 'td':
            if self.currentCell not in self.cellsToIgnore:
                self.readCurrentCell = True
        
        
        
        
    def handle_endtag(self, tag):
        
        if tag == 'td':
            if self.readCurrentCell:
                self.extractedDataOfCurrentRow.append(''.join(self.currentData))
                self.currentData.clear()
                self.readCurrentCell = False
                
            if self.readCurrentRow:
                self.currentCell += 1
            
        if tag == 'tr':
            if self.readCurrentRow:
                self.extractedData.append(self.extractedDataOfCurrentRow)
                self.extractedDataOfCurrentRow = []
                self.readCurrentRow = False
                
            if self.isInsideTable:
                self.currentRow += 1;
                
                
        if self.isInsideTable and tag == 'table':
            self.isInsideTable = False
        
        if self.isInsideDiv and tag == 'div':
            self.isInsideDiv = False
                 
            
    def handle_data(self, data):
        if self.readCurrentCell:
            self.currentData.append(data)
        
        