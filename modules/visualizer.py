import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

def pie_chart(data, title, path):
   
    if not data:
        print("No data to create pie chart!")
        return
    
    plt.figure(figsize=(10, 8))

    labels = list(data.keys())
    vals = list(data.values())

   
    import matplotlib.cm as cm
    colors = cm.get_cmap('Set3')(range(len(labels)))

    plt.pie(vals, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title(title, fontsize=16, fontweight='bold')

    plt.tight_layout() 
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Pie chart saved: {path}")


def line_chart(data, title, x, y, path):
   
    if not data:
        print("No data to create line chart!")
        return
    
    plt.figure(figsize=(14, 6))

    items = sorted(data.items())

    a = [i[0] for i in items]
    b = [i[1] for i in items]

    plt.plot(a, b, marker='o', linewidth=2, markersize=8, color='green')

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)
    plt.grid(True, alpha=0.3)

    plt.tight_layout() 
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Line chart saved: {path}")


def bar_chart(data, title, x, y, path):
    """Make a bar chart"""
    if not data:
        print("No data for bar chart!")
        return
    
    plt.figure(figsize=(12, 6))
    labels = list(data.keys())
    vals = list(data.values())

    plt.bar(labels, vals, color='steelblue', edgecolor='black')

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10) 
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout() 
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Bar chart saved: {path}")


def scatter_chart(data, title, x, y, path):
    """Make a scatter chart"""
    if not data:
        print("No data to create scatter chart!")
        return
    
    import numpy as np

    plt.figure(figsize=(14, 6))

    items = sorted(data.items())
    a = [i[0] for i in items]
    b = [i[1] for i in items]

    plt.scatter(a, b, s=100, alpha=0.6, c='blue', edgecolors='black')

    if len(a) > 1:
        m, n = np.polyfit(a, b, 1)
        plt.plot(a, m * np.array(a) + n, "r--", linewidth=2, label='Trend')
        plt.legend()

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x, fontsize=12)
    plt.ylabel(y, fontsize=12)
    plt.grid(True, alpha=0.3)

    plt.tight_layout() 
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Scatter chart saved: {path}")