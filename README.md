

---

# Web Scraping Workflow Readme

This repository contains scripts and instructions for a web scraping workflow to extract data from web pages and organize it into a structured format. The workflow involves several steps, each with its own script and purpose.

## Workflow Steps

### Step 1: Save Page Content with Image URLs

- **Script:** `step_1_sc_save_page_wise.py`
- **Input:** [None](https://shop.adidas.jp/men/)
- **Output File:** `dis_man_1.csv`
- **Output Columns:** `href` (page URL), `src` (image URL)

### Step 2: Properly Format Page URLs

- **Script:** `step_2_make_proper_href.py`
- **Input:** `dis_man_1.csv`
- **Output File:** `dis_man_1_href.csv`
- **Output Columns:** `href`, `src`, `complete_url` (proper HTTP URL)

### Step 3: Extract Product Details

- **Script:** `step3_easy_columns.py`
- **Input:** `dis_man_1_href.csv`
- **Output File:** `product_details.csv`
- **Output Columns:** `Breadcrumb(Category)`, `Category`, `Product name`, `Pricing`, `Available size`, `url`

### Step 4: Extract Table Data and Ratings

#### Option 1: Dynamically Extract Data

- **Script:** `step_4_option_1_table_and_rating_and_command.py`
- **Input:** `dis_man_1_href.csv`
- **Output File:** `table_data.csv`
- **Output Columns:** `url`, `title_of_description`, `general_description_of_the_product`, `General_description(itemization)`, `size_information_table_header`, `size_information_data`, `Rating`, `Number of Reviews`, `Recommended rate`, `keywords`

#### Option 2: Manually Scroll to Load Data

- **Script:** `step_4_option_2_table_and_rating_and_command.py`
- **Input:** `test.html` (Manually insert HTML body and associate product details URL)
- **Output File:** Append data into `table_data.csv`
- **Output Columns:** Same as Option 1

### Merging and Finalization

- Merge `dis_man_1.csv`, `product_details.csv`, and `table_data.csv` using the common column `url` or `complete_url`.
- Rearrange the column sequence if needed and rename columns using Pandas.
- Save the merged data as `result.csv`.

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Run each script in sequence according to the workflow steps outlined above.
4. Follow any additional instructions provided within each script or step.
5. After completing all steps, access the final merged data in `result.csv`.

## Dependencies

- Python 3.x
- Pandas
- (Add any additional dependencies if required)

## License

This project is licensed under the [MIT License](LICENSE).

---

Feel free to customize this README to suit your specific project requirements and provide additional information or instructions as needed.
