
# 18. This program builds fake sales data that is realistic
#     for the Hartwell Group demo. Their legal team
#     blocked the transfer of any real transaction data for the demo phase.

# 19. What files does it read? What files does it create?
#     it reads  business_lists.txt and creates business_data.csv
#     business_data_set_2.csv.

# 20. The ten dataset fields and what they mean:
#     TransactionID    unique ID number for each sale
#     Region           the 5 sale regions
#     CustomerType     kind of customer bought it
#     ProductCategory  product category was sold
#     SalesChannel     how the sale was made 
#     UnitsSold        randomlly assigned, units 1-100 
#     UnitPrice        randomly assigned,  $5.00 to $2500.00
#     DiscountApplied  randomly assigned, yes or no 
#     PurchaseTotal    units * price minus discount if yes
#     RiskFlag         Low  Medium  High based on PurchaseTotal

# 21. What each function does:
#     read_business_lists()       reads the txt file returns  lists
#     get_positive_integer()      validates number
#     calculate_purchase_total()  does the math for total with discount
#     assign_risk_flag()          figures out Low Medium High
#     generate_record()           builds one full transaction row
#     generate_dataset()          calls generate_record() over and over
#     save_to_csv()               writes everything to a csv file
#     read_csv()                  reads a csv file back in
#     get_price_range()           puts a dollar amount into a bucket
#     analyze_distributions()     counts how often each value shows up
#     build_sampling_pools()      turns counts into weighted lists
#     print_distribution_report() prints countpercent table for one field
#     print_comparison()          prints file1 vs file2 percentages

# 22.  How does the second dataset get its behavior from the first?
# After phase 2 counts how many times each value appeared in file 1,
# phase 3 builds a list where each value shows up the same amount of times.
#So if North appeared 170 times out of 1500 records it takes up 170 spots in the pool.

#
# 23. What real business decisions could this kind of data support?
#   You could use this to train new employees to stay up to date or other companies that a similar
#   problems or databases.

#
# 24. 1. There aren't any dates for sales, all businesses have date of sales.
#     2. Since it is randomized and not real the numbers and combos can be unrealistic.


import random



def read_business_lists(filename):

    regions = []
    customer_types = []
    product_categories = []
    sales_channels = []
    file_loaded = False

    try:
        infile = open(filename, "r")
        file_loaded = True

        for line in infile:
            line = line.strip()

            if "=" not in line:
                continue

            parts = line.split("=", 1)
            var_name = parts[0].strip()
            right_side = parts[1].strip()

            right_side = right_side.replace("[", "").replace("]", "")

            raw_items = right_side.split(",")
            clean_items = []
            for item in raw_items:
                item = item.strip().strip('"}').strip("'")
                if item != "":
                    clean_items.append(item)

            if var_name == "regions":
                regions = clean_items
            elif var_name == "customer_types":
                customer_types = clean_items
            elif var_name == "product_categories":
                product_categories = clean_items
            elif var_name == "sales_channels":
                sales_channels = clean_items

        infile.close()

    except FileNotFoundError:
        print()
        print("ERROR: Could not find business_lists.txt")
        print("Please put business_lists.txt in the same folder as this program.")
        print("The program cannot run without it.")
    except Exception as e:
        print("Something went wrong reading business_lists.txt:", e)

    return regions, customer_types, product_categories, sales_channels, file_loaded


# just loop until the user puts in a number that makes sense
def get_positive_integer(prompt):

    while True:
        answer = input(prompt).strip()

        try:
            num = int(answer)
        except ValueError:
            print("That is not a valid number. Please try again.")
            continue

        if num <= 0:
            print("The number has to be greater than zero.")
            continue

        return num


# total math and  discount if applicable
def calculate_purchase_total(units, price, discount):

    total = units * price

    if discount == "Yes":
        pct = random.randint(5, 25) / 100
        total = total * (1 - pct)

    return round(total, 2)


# checks total and assigns a risk level
def assign_risk_flag(total):

    if total < 1000.00:
        return "Low"
    elif total < 10000.00:
        return "Medium"
    else:
        return "High"


# put together sale record

def generate_record(source, transaction_id, use_pools=False):

    if use_pools:
        region    = random.choice(source["Region"])
        cust_type = random.choice(source["CustomerType"])
        prod_cat  = random.choice(source["ProductCategory"])
        channel   = random.choice(source["SalesChannel"])
        units     = random.choice(source["UnitsSold"])
        price     = random.choice(source["UnitPrice"])
        discount  = random.choice(source["DiscountApplied"])
    else:
        regions, customer_types, product_categories, sales_channels = source
        region    = random.choice(regions)
        cust_type = random.choice(customer_types)
        prod_cat  = random.choice(product_categories)
        channel   = random.choice(sales_channels)
        units     = random.randint(1, 100)
        price     = round(random.uniform(5.00, 2500.00), 2)
        discount  = random.choice(["Yes", "No"])

    total = calculate_purchase_total(units, price, discount)
    risk  = assign_risk_flag(total)

    record = [transaction_id, region, cust_type, prod_cat, channel,
              units, price, discount, total, risk]

    return record


# run generate_record and collect all the rows
def generate_dataset(source, count, start_id, use_pools=False):

    all_records = []
    i = 0

    while i < count:
        row = generate_record(source, start_id + i, use_pools)
        all_records.append(row)
        i += 1

    return all_records


# save everything to a csv file 
def save_to_csv(filename, headers, records):

    try:
        outfile = open(filename, "w")

        outfile.write(",".join(headers) + "\n")

        for record in records:
            row = []
            for field in record:
                row.append(str(field))
            outfile.write(",".join(row) + "\n")

        outfile.close()
        print("Saved:", filename)

    except Exception as e:
        print("Could not write to", filename)
        print("Error:", e)


# read  csv back in and gives us all the rows
def read_csv(filename):

    rows = []

    try:
        infile = open(filename, "r")
        first = True

        for line in infile:
            if first:
                first = False
                continue
            line = line.strip()
            if line != "":
                rows.append(line.split(","))

        infile.close()

    except FileNotFoundError:
        print("Could not find file:", filename)
    except Exception as e:
        print("Problem reading", filename, "-", e)

    return rows


# take  dollar amount and figure out which price range it goes in
def get_price_range(val):

    if val < 1000:
        return "Under $1,000"
    elif val < 5000:
        return "$1,000 to $4,999"
    elif val < 10000:
        return "$5,000 to $9,999"
    elif val < 25000:
        return "$10,000 to $24,999"
    else:
        return "$25,000 and above"


# go through every row and count how many times each value is there
# unitprice and purchasetotal get put into ranges 
def analyze_distributions(headers, rows):

    range_fields = ["UnitPrice", "PurchaseTotal"]

    dists = {}
    for h in headers:
        if h != "TransactionID":
            dists[h] = {}

    for row in rows:
        if len(row) < len(headers):
            continue

        for i in range(len(headers)):
            field = headers[i]

            if field == "TransactionID":
                continue

            raw = row[i].strip()

            try:
                if field in range_fields:
                    key = get_price_range(float(raw))
                elif field == "UnitsSold":
                    val = int(raw)
                    if val <= 10:
                        key = "1 to 10"
                    elif val <= 25:
                        key = "11 to 25"
                    elif val <= 50:
                        key = "26 to 50"
                    elif val <= 75:
                        key = "51 to 75"
                    else:
                        key = "76 to 100"
                else:
                    key = raw
            except Exception:
                key = raw

            if key in dists[field]:
                dists[field][key] += 1
            else:
                dists[field][key] = 1

    return dists


# turn the frequency count into big  lists
# if North showed up 170 times it gets 170 spots in the pool

def build_sampling_pools(dists, original_rows, headers):

    pools = {}
    dont_pool = ["RiskFlag", "PurchaseTotal", "UnitsSold", "UnitPrice"]

    for field in dists:
        if field in dont_pool:
            continue
        pool = []
        for value in dists[field]:
            count = dists[field][value]
            j = 0
            while j < count:
                pool.append(value)
                j += 1
        pools[field] = pool

    # unitssold and unitprice come straight from the actual values in file 1
    units_idx = -1
    price_idx = -1

    for i in range(len(headers)):
        if headers[i] == "UnitsSold":
            units_idx = i
        if headers[i] == "UnitPrice":
            price_idx = i

    units_pool = []
    price_pool = []

    for row in original_rows:
        try:
            units_pool.append(int(row[units_idx].strip()))
            price_pool.append(float(row[price_idx].strip()))
        except Exception:
            continue

    pools["UnitsSold"] = units_pool
    pools["UnitPrice"] = price_pool

    return pools


# prints out the count and percentage breakdown for one field
def print_distribution_report(field_name, dist, total):

    print()
    print(field_name.upper() + " DISTRIBUTION  (" + str(total) + " records)")
    print("-" * 48)

    for value in dist:
        count = dist[value]
        pct = (count / total) * 100
        print("  {:<24} {:>6}   {:>5.1f}%".format(value, count, pct))


# show file 1 and file 2 percentages next to each other
def print_comparison(field_name, dist1, dist2, total1, total2):

    print()
    print(field_name.upper() + " DISTRIBUTION COMPARISON")
    print("-" * 52)
    print("  {:<22} {:>10}  {:>10}".format("", "File 1", "File 2"))

    all_keys = []
    for k in dist1:
        if k not in all_keys:
            all_keys.append(k)
    for k in dist2:
        if k not in all_keys:
            all_keys.append(k)

    for key in all_keys:
        c1 = dist1.get(key, 0)
        c2 = dist2.get(key, 0)
        p1 = (c1 / total1 * 100) if total1 > 0 else 0
        p2 = (c2 / total2 * 100) if total2 > 0 else 0
        print("  {:<22} {:>9.1f}%  {:>9.1f}%".format(key, p1, p2))


# runs everything in order just calls the other functions one by one
def main():

    headers = ["TransactionID", "Region", "CustomerType", "ProductCategory",
               "SalesChannel", "UnitsSold", "UnitPrice", "DiscountApplied",
               "PurchaseTotal", "RiskFlag"]

    file1_name  = "business_data.csv"
    file2_name  = "business_data_set_2.csv"
    lists_file  = "business_lists.txt"
    file1_start = 100001
    file2_start = 200001

    compare_fields = ["Region", "CustomerType", "ProductCategory",
                      "SalesChannel", "DiscountApplied", "RiskFlag"]

    
    # PHASE 1 - generate the original dataset
    
    print()
    print("PHASE 1 - Building Original Dataset")
    

    regions, customer_types, product_categories, sales_channels, file_loaded = read_business_lists(lists_file)

    if not file_loaded:
        print()
        print("Program stopped. Fix the file issue above and try again.")
        return

    print("Loaded lists from", lists_file)
    print("Regions:", regions)
    print("Customer Types:", customer_types)
    print("Categories:", product_categories)
    print("Channels:", sales_channels)
    print()

    while True:
        count1 = get_positive_integer("How many records for File 1? (50 to 50000): ")
        if count1 < 50 or count1 > 50000:
            print("Has to be between 50 and 50,000. Try again.")
        else:
            break

    print("Generating", count1, "records...")
    source1  = (regions, customer_types, product_categories, sales_channels)
    records1 = generate_dataset(source1, count1, file1_start, use_pools=False)
    save_to_csv(file1_name, headers, records1)

   
    # PHASE 2 - analyze the file we just built
    
    print()
    print("PHASE 2 - Analyzing File 1")
    

    rows1  = read_csv(file1_name)
    total1 = len(rows1)
    dist1  = analyze_distributions(headers, rows1)

    for field in headers:
        if field == "TransactionID":
            continue
        if field in dist1:
            print_distribution_report(field, dist1[field], total1)

    # 
    # BUSINESS INTERPRETATION
    # based on a test run with 1500 records
    #
    # Q9 - Which region had the most transactions?
    #   North had the most with 372 records.
    
    # Q10 - Which customer type showed up most?
    #   Retail was highest near 22% but all five types were
    #   close to 20%. 
    
    # Q11 - How often were discounts applied?
    #   Discounts were applied about 50% of the time. 
    #
    # Q12 - Was most risk Low Medium or High?
    #   High risk was almost in every single transaction. It was at 82%. 
    

    
    # PHASE 3 - build the sampling pools
   
    print()
    print("PHASE 3 - Building Sampling Pools")
    

    pools = build_sampling_pools(dist1, rows1, headers)

    for field_name in pools:
        print("Pool built for", field_name, "-", len(pools[field_name]), "entries")

    
    # PHASE 4 - generate the second dataset from the pools
    
    print()
    print("PHASE 4 - Generating File 2")
    

    count2 = get_positive_integer("How many records for the new dataset? ")

    print("Generating", count2, "records using sampling pools...")
    records2 = generate_dataset(pools, count2, file2_start, use_pools=True)
    save_to_csv(file2_name, headers, records2)

    
    ## PHASE 5 - validate that file 2 matches file 1
    
    print()
    print("PHASE 5 - Validation Report")
  

    rows2  = read_csv(file2_name)
    total2 = len(rows2)
    dist2  = analyze_distributions(headers, rows2)

    for field in compare_fields:
        if field in dist1 and field in dist2:
            print_comparison(field, dist1[field], dist2[field], total1, total2)

    print()
    print("Done. Check your folder for the two csv files.")

    ## loop to rerun
    print()
    again = input("Would you like to generate more records? (yes or no): ").strip().lower()

    if again == "yes" or again == "y":
        print()
        print("Starting over...")
        print()
        main()
    else:
        print()
        print("Done. Thanks for using the Sales Data Generator!")


main()


# ==============================================================
# TESTING LOG
# ==============================================================
#
# Test Run 1 - small, 100 records file 1, 100 records file 2
#   -made sure the basic logic was right before going further.
#   -All 10 fields showed up in the csv.
#   -Opened it in Excel and spot checked a few rows to confirm PurchaseTotal matched
#   -units * price and that RiskFlag matched the total correctly.

  

# Test Run 2 - medium, 2000 records file 1, 1500 records file 2
#   -Distributions in phase 2 looked more consistent 
#   -All 5 regions landed between 18% and 22%. Discount split was right at 50/50.
#   -Phase 5 comparison showed all 6 fields matching within about 2 percentage points. 


#
# Test Run 3 - large, 25000 records file 1, 20000 records file 2
#   -Ran all the way through without any errors
#   -Most fields in the comparison report matched within 1 to 2 percent of each other.
#   -RiskFlag had the biggest gap at about 1.5% because it gets recalculated

#

# BUSINESS REFLECTION - To M. Okafor

#
# Q28 - How else could PRS use this beyond the Hartwell demo?
#   I think the biggest use is  testing new dashboard
#   features before a client goes live.  With this you can
#   generate 50,000 records that behave like the client and run
#   real tests against that. A second use is onboarding new clients
#   who want to see the platform before committing. Instead of
#   showing them another client's data you can make up a synthetic
#   version that is close to their industry. It doesn't raise any concerns.
# Q29 - What patterns showed up that were notable?
#   . I expected a fairly even spread of Low, Medium, and High but High ended up
#   at around 82% in my larger test runs. Once I worked through
#   the math it made sense. The unit prices were up to $2500 and unit
#   counts up to 100, most combinations produced a total well above
#   $10,000 which is the max for the high. Low risk only happened
#   when  the price and quantity were small at the same time.
#   That combination came in around 2%.
#   The 50/50 discount was also very noteable.

# Q30 - Did file 2 successfully reproduce file 1's profile?
#   Yes. In my 25000/20000 run most fields were within about 1 to 2 percent of each other.
#   Region was the closest, with North sitting at 19.8% in
#   file 1 and 20.3% in file 2. CustomerType was also very close, with
#   no category being different by more than 1.4%. DiscountApplied came
#   in at 51.2% yes in file 1 and 50.7% in file 2 which is about
#   as close as you can  expect. RiskFlag had the widest gap.

 

# Q31 - Two real limitations of this simulation:

#   In real Hartwell data there are probably patterns where certain
#   customer types prefer certain channels or buy certain products.
#   To fix this you would need to track pairs or
#   groups of values to get to your target.
#   The second issue is there are no dates anywhere in the records.
#   Without dates everything looks perfectly flat over time.


