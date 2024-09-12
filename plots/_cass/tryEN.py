import matplotlib.pyplot as plt

# set font parameters to render with LaTeX
plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 20

plt.rcParams['xtick.major.size'] = 7 #set the value globally
plt.rcParams['xtick.minor.size'] = 5 #set the value globally
plt.rcParams['ytick.major.size'] = 7 #set the value globally

# iterate over the input files
for i in range(1, 4):
    # load the data from the input files
    with open(f"{i}.txt") as f1, open(f"{i+3}.txt") as f2:
        data1 = [[float(x) for x in line.strip().split()] for line in f1]
        data2 = [[float(x) for x in line.strip().split()] for line in f2]
    
    # extract x and y values for each staircase function
    x1 = []
    y1 = []
    prev_y1 = 0
    for row in data1:
        x1.append(row[3])
        if row[2] > prev_y1:
            y1.append(row[2])
            prev_y1 = row[2]
        else:
            y1.append(prev_y1)

    x2 = []
    y2 = []
    prev_y2 = 0
    for row in data2:
        x2.append(row[3])
        if row[2] > prev_y2:
            y2.append(row[2])
            prev_y2 = row[2]
        else:
            y2.append(prev_y2)		
           
    # plot the staircase functions
    fig, ax = plt.subplots(figsize=(6, 5.5))
   
    ax.set_xlim(left=0, right=max([x1[-1], x2[-1]])+5)
    ax.set_ylim(bottom=80, top=140)
    
    ax.plot(x1, y1, drawstyle="steps-post", label=r"NM", color='blue')
    ax.plot(x2, y2, drawstyle="steps-post", label=r"L-BFGS", color='red')
    
    # add labels and legend
    ax.set_xlabel(r"\# $f$", fontsize=22)
    ax.set_ylabel(r"Result approximation", fontsize=22)
    # ax.set_title(f"Staircase plot {i}")
    
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.24),
          fancybox=True, shadow=False, ncol=2)
    
    fig.tight_layout()
    
    # save the plot to a file
    plt.savefig(f"{i + 5}.pdf")

