#Start by opening the file and creating blank lists for each variable of interest.

bike_data = open("bikeshare_data_2022project.csv", "r")
bikes = bike_data.readlines()
bikes.pop(0) #Get rid of headers

day_num = []
month = []
temp = []
feel_temp = []
count_unclean = []
count = []

#Now, set up each variable of interest.

for i in range(len(bikes)):
    aline = bikes[i]
    values = aline.split(",")

    day_num.append(int(values[0]))
    month.append(int(values[4]))
    feel_temp.append(float(values[10]))
    count_unclean.append(values[15])

for value in count_unclean:
    value_clean = value.strip()
    count.append(int(value_clean))

#LINEAR REGRESSION - ONE X VARIABLE

#Define linear regression functions: compute one y value, compute all y values, and compute MSE.

def compute_y(x, m, b):
    y = m * x + b
    return y

def compute_all_y(list_of_x, m, b):
    list_of_y = []
    for x in list_of_x:
        y = compute_y(x, m, b)
        list_of_y.append(y)
    return list_of_y

def compute_mse(list_of_known, list_of_predictions):
    se = 0
    for i in range(len(list_of_known)):
        se += (list_of_predictions[i] - list_of_known[i])**2
    mse = se / len(list_of_known)
    return mse

#Define the step, initial slope, and initial intercept. Get initial predicted counts and MSE.

step = 0.01
trials = 10000
m = 8
b = 950

pred_count = compute_all_y(day_num, m, b)
mse = compute_mse(count, pred_count)

#Adjust slope and intercept until MSE is as small as possible.

for i in range(trials):
    temp_m = m + step
    temp_pred_count = compute_all_y(day_num, temp_m, b)
    temp_mse = compute_mse(count, temp_pred_count)

    # if MSE gets smaller, adjust slope in same direction as before, use this m
    # compare mse and temp_mse
    # if temp_mse is better, m = temp_m and mse = temp_mse
    if temp_mse < mse:
        m = temp_m
        mse = temp_mse
        pred_count = temp_pred_count

    # if MSE gets bigger, adjust slope in opposite direction, make m bigger
    else:
        temp_m = m - step
        temp_pred_count = compute_all_y(day_num, temp_m, b)
        temp_mse = compute_mse(count, temp_pred_count)

        if temp_mse < mse:
            m = temp_m
            mse = temp_mse
            pred_count = temp_pred_count

    # do again for b: bigger MSE make b smaller
    temp_b = b + step
    temp_pred_count = compute_all_y(day_num, m, temp_b)
    temp_mse = compute_mse(count, temp_pred_count)

    if temp_mse < mse:
        b = temp_b
        mse = temp_mse
        pred_count = temp_pred_count

    # if MSE gets bigger, adjust slope in opposite direction, make m bigger
    else:
        temp_b = b - step
        temp_pred_count = compute_all_y(day_num, m, temp_b)
        temp_mse = compute_mse(count, temp_pred_count)

        if temp_mse < mse:
            b = temp_b
            mse = temp_mse
            pred_count = temp_pred_count

#Final results

print("LINEAR REGRESSION")
print("Final intercept:", b)
print("Final slope:", m)
print("Final MSE:", mse)

#MULTIPLE REGRESSION - MULTIPLE X VARIABLES

#Set up multiple regression functions: dot product, compute MSE, and fit (finds best coefficient for a line for multiple regression).

# Define dot product
def dot(a, b):
    accum = 0
    for i in range(len(a)):
        y = a[i] * b[i]
        accum += y
    return accum

# Define mean square error function (we did this in the last lab)
def compute_mse(list_of_known, list_of_predictions):
    se = 0
    for i in range(len(list_of_known)):
        se += (list_of_predictions[i] - list_of_known[i])**2
    mse = se / len(list_of_known)
    return mse

# Define a function fit(data table of xvalues, known yvalues, trials) and returns a model (the model is the list [c1, c2, c3] of coefficients in the line we find with smallest mse)
def fit(x_vals, y_vals, trials):
    # theta will be what we call the list of coefficients for a line
    theta_best = [100, 100, 100] # you need to find a good initial guess for the list of coefficients

    pred_y = []
    for t in range(len(x_vals)):
        pred_y.append(dot(theta_best, x_vals[t]))

    mse = compute_mse(y_vals, pred_y)

    for j in range(trials):
        for i in range(len(theta_best)):
        # For each coefficient we check if adding learn rate to the coefficent makes mse go down and if subtracting the learn makes the mse go down
            #Add
            theta_add = theta_best[i] + step

            theta_best_add = theta_best[:]
            theta_best_add[i] = theta_add

            pred_y_add = []
            for t in range(len(x_vals)):
                pred_y_add.append(dot(theta_best_add, x_vals[t]))

            temp_mse_add = compute_mse(y_vals, pred_y_add)

            #Subtract
            theta_sub = theta_best[i] - step

            theta_best_sub = theta_best[:]
            theta_best_sub[i] = theta_sub

            pred_y_sub = []
            for t in range(len(x_vals)):
                pred_y_sub.append(dot(theta_best_sub, x_vals[t]))

            temp_mse_sub = compute_mse(y_vals, pred_y_sub)

            # pick the value of those 3 that gives smallest mse, use that to redefine theta_best
            if temp_mse_add < temp_mse_sub and temp_mse_add < mse:
                theta_best = theta_best_add
                pred_y = pred_y_add
                mse = temp_mse_add

            elif temp_mse_sub < mse:
                theta_best = theta_best_sub
                pred_y = pred_y_sub
                mse = temp_mse_sub

    return theta_best, mse

#Set up the x-values, which is a list of lists (we'll be using month and feel temp x-variables).

x_vals = []

for i in range(len(count)):
    entry = []
    entry.append(1)
    entry.append(month[i])
    entry.append(feel_temp[i])
    x_vals.append(entry)

#Define step and number of trials, then print theta best (list of coefficients) and MSE.

step = 1
trials = 10000

results = fit(x_vals, count, trials)

#Final results

print("\nMULTIPLE REGRESSION")
print("Final coefficients:", results[0])
print("Final MSE:", results[1])

#Close file

bike_data.close()