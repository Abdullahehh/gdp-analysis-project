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


