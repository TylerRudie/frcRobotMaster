

class frcBOM(object):

    def __init__(self,
                 name,
                 cost,
                 items=[]):

        self.cost = cost
        self.name = name
        self.items = items

    def toMarkdown(self):
        string = '### {0} ::          Cost : ${1}'.format(self.name,
                                                          self.cost)
        string = '{0}\nDescription|Material|Manufacturer|Quantity|Measurement|Market Price|Total Price'.format(string)
        string = '{0}\n:---|:---|:---|:---|:---|:---|---:'.format(string)
        for line in self.items:
            string = "{0}\n{1}|{2}|{3}|{4}|{5}|{6}|{7}".format(string,
                                                                line['details__shortDescription'],
                                                                line['details__material__name'],
                                                                line['details__manufacturer__name'],
                                                                line['quantity'],
                                                                line['details__measurement'],
                                                                line['details__marketPrice'],
                                                                line['totalPrice']
                                                                 )
        return string
