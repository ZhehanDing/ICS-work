def main():
     a = 2

     def apple():
         global  a
         a = 1
     apple()
     print(a)
main()
