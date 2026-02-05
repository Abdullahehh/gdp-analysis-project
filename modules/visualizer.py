import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def pie_chart(data,title,path):
    """Make a pie chart"""
    if not data:
        print("No data to create pie chart!")
        return
    
    plt.figure(figsize=(10,8))

    labels=list(data.keys())
    vals=list(data.values())

    colors= ['#ff9999','#66b3ff','#99ff99','#ff99cc']

    plt.pie(vals,labels=labels, autopct='%1.1f%%', colors=colors,startangle=90)
    plt.title(title,fontsize=16,fontweight='bold')

    plt.savefig(path,dpi=300,bbox_inches='tight')
    plt.close()
    print(f" Pie chart saved: {path}")

def line_chart(data,title,x,y,path):
    """Make a line chart"""
    if not data:
        print("No data to create line chart!")
        return
    
    plt.figure(figsize=(14,6))

    items=sorted(data.items())

    a=[i[0] for i in items]
    b=[i[1] for i in items]

    plt.plot(a,b,marker='o',linewidth=2,markersize=8,color='green')

    plt.title(title,fontsize=16,fontweight='bold')
    plt.xlabel(x,fontsize=12)
    plt.ylabel(y,fontsize=12)
    plt.grid(True,alpha=0.3)

    plt.savefig(path,dpi=300,bbox_inches='tight')
    plt.close()
    print(f" Line chart saved: {path}")

