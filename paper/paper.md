---
title: "SkyRank: A Framework for Multi-Criteria Decision in Databases"
tags:
  - multi-criteria decision analysis
  - benchmarking
  - databases
  - skyline
authors:
  - name: Nael Turlure
    orcid: 0009-0005-9978-5163
    affiliation: 1
  - name: Mickaël Martin Nevot
    orcid: 0009-0004-7893-3449
    affiliation: 1
affiliations:
  - name: Aix-Marseille Université, France
    index: 1
date: 26 May 2025
bibliography: paper.bib
---

# Summary

Multi-criteria decision analysis in databases has been actively studied, especially through the Skyline operator. Yet, few approaches offer a relevant comparison of Pareto optimal, or Skyline, points for high cardinality result sets.

We propose to improve the **dp-idp** method — inspired by tf-idf — which computes a score for each Skyline point, by introducing the concept of **dominance hierarchy**. As dp-idp lacks efficiency and does not ensure a distinctive rank, we introduce **RankSky**, an adaptation of Google’s PageRank algorithm using a square stochastic matrix, teleportation matrix, damping factor, and row score eigenvector (computed via the IPL algorithm).

To complement this, we propose **CoSky**, a TOPSIS-based method designed to be embeddable in database management systems. It relies on automatic attribute weighting via the **Gini index**, then computes a cosine-based score (Salton’s similarity) toward an ideal solution.

Finally, we present **DeepSky**, a framework that combines multi-level Skyline queries with dp-idp, RankSky, or CoSky. All three methods (dp-idp, RankSky, and CoSky) are implemented and evaluated experimentally.

# Acknowledgements

We thank our colleagues and mentors from Aix-Marseille Université for their insights during the development of this work.

# References
