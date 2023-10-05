# Summary

Goal: Enable massive and comprehensive literary search by searching multiple sources (peer reviewed papars, editorials, social media, papers in other languages, etc) for a list of topics and compiling the results in a zotero database. 

### Example usage
"The Whole Student" mental health research team designed and implemented a novel literature review process designed to eliminate bias and achieve comprehensiveness by drawing from a pre-screening collection of 1071 academic papers, articles, and multimedia sources, the majority of which are available here under the queries_folder directory. The literature review process for a topic intimately connected with its researchers faces threats from experiential bias and domain knowledge bias. Also, literature review with any large research team faces the problem of topic clustering, which severely limits the review's comprehensiveness. (Topic clustering is where multiple members overlap on literature review research leading to both decreased efficiency and decreased comprehensiveness.)

By building a comprehensive database of keywords through careful evaluation and designing a computer algorithm to target each topic in the context of undergraduates and mental health, we solve both problems. This algorithm produced 923 pieces of material and an additional 148 were procured by team members from sources such as video, multimedia, and government records, which the algorithm has a limited ability to identify. The sourced material was divided into 51 topics, which were randomly assigned to members for screening to prevent domain knowledge bias. Members screened material through title and abstract based on relevance, selecting 10% of materials to contribute to our analysis.  

## Overview

Welcome to the Literature Search Engine! This readme provides an overview of the code and components that power this search engine. The code ties together various functionalities to streamline the process of conducting literature searches, processing queries, reading publications, and integrating with Zotero.

## Code Structure

The core of the system is written in Python and utilizes several libraries and tools. Let's break down the key components:

### 1. `gradio` and User Interface

The code uses the `gradio` library to create a user-friendly interface for interacting with the search engine. Users can select various options, such as processing queries, reading publications, and adding results to Zotero.

### 2. Query Generation

The search engine generates queries based on keywords provided in a specific format. The keywords document serves as input to build queries for Google Scholar. The format includes constraints and subtopics, which help create focused and relevant search queries.

### 3. Scholarly API

The `scholarly` library is used to interact with Google Scholar. It allows the system to search for publications and retrieve relevant information.

### 4. Zotero Integration

The code integrates with Zotero, a reference management tool. It can add search results to a specific Zotero collection for easy organization and reference management.

### 5. Workflow Control

The code provides options to control the workflow, including processing queries, reading publications, and adding them to Zotero. These options can be selected through checkboxes in the user interface.

## How to Use

To use the Literature Search Engine, follow these steps:

1. Ensure you have the necessary Python libraries installed, including `gradio`, `pyzotero`, and `scholarly`.

2. Structure your keywords document in the specified format with constraints and subtopics.

3. Run the code with the appropriate options selected in the user interface.

4. The search engine will generate queries, retrieve publications, and optionally add them to Zotero based on your selections.

## Customization

You can customize the search engine by modifying the keywords document and adjusting the code to fit your specific needs. Additionally, you can integrate other APIs or databases for broader literature searches.

## Future Development

Considering the following potential improvements and extensions:

- Enhance the user interface for better user experience and feedback.
- Implement more advanced search strategies, such as relevance ranking.
- Explore additional integration options with reference management tools or databases.

## Feedback and Support

Your feedback is valuable! If you encounter any issues, have suggestions, or need assistance, please reach out to me for support.

## Acknowledgments

This Literature Search Engine was developed to assist researchers and academics in their quest for knowledge. I hope it proves to be a valuable tool in your scholarly endeavors.
