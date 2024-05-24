# K-Means Clustering using MapReduce

## Assignment Overview

This repository contains the implementation of the K-Means clustering algorithm using the MapReduce framework from scratch for the Winter 2024 CSE530 Distributed Systems assignment. The goal is to partition a given dataset into K clusters in a distributed manner.

## Problem Statement

The task involves implementing the K-Means algorithm using the MapReduce model. This includes setting up a master process responsible for coordinating mappers and reducers, writing mapper and reducer processes, and handling fault tolerance scenarios.

## Implementation Details

### Components:

1. **Master**: Coordinates the execution of mappers and reducers, initializes centroids, and manages iterations.
2. **Mapper**: Reads input data splits, applies the Map function to generate intermediate key-value pairs, partitions the output, and writes to local files.
3. **Reducer**: Sorts and groups intermediate key-value pairs, applies the Reduce function to generate final key-value pairs, and writes to local files.
4. **Input Split**: Divides the input data into smaller chunks for parallel processing by mappers.
5. **Partitioning**: Distributes key-value pairs evenly among reducers.
6. **Shuffle and Sort**: Sorts and groups intermediate key-value pairs by key for reduction.
7. **Centroid Compilation**: Compiles the final list of centroids by parsing output files from reducers.

### Setup:

- Each mapper, reducer, and the master is a separate process running on the same machine.
- gRPC is used for communication between processes.
- The master initiates the execution with parameters like the number of mappers, reducers, centroids, and iterations.

### Fault Tolerance:

- Handles failures associated with mapper or reducer processes by re-running tasks if necessary.

### Sample Input and Output:

- Input data is divided into chunks for parallel processing.
- Intermediate and final output files are generated according to a specified format.

## Deliverables

Please submit a zipped file containing the entire codebase with the given directory structure.

## Evaluation

Your implementation will be evaluated based on the following criteria:

- Testing with different configurations of mappers, reducers, centroids, and iterations.
- Correctness of mapper and reducer outputs for various configurations.

## Instructions

- Ensure all components are running as separate processes on the same machine.
- Use gRPC for communication between processes.
- Log/print relevant information for easy debugging and monitoring.
- Test thoroughly with different configurations before submission.

---

For detailed specifications and instructions, refer to the assignment documentation provided.
https://docs.google.com/document/d/e/2PACX-1vQ6UvQzah5o2mcVjFpb6llZrOaqPz6PiQ4m_7zYlRDeYdHWJ77ziYN22-HyE0VDnHBxojsHPnqu1nf7/pub
