# Student and Supervisor Allocation - Pareto Optimal approach

An AI tool in pure python capable of matching 400+ final year students with 60+ dissertation supervisors using Genetic Algorithm. It can find optimal solutions from a massive 400^60+ size search space in minutes. 

This project is a package for student to supervisor allocation, a variant of the college admission problem. 

[![Known Vulnerabilities](https://snyk.io/test/github/rithinch/pareto-optimal-student-supervisor-allocation/badge.svg?targetFile=pystsup/requirements.txt)](https://snyk.io/test/github/rithinch/pareto-optimal-student-supervisor-allocation?targetFile=pystsup/requirements.txt)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rithinch_pareto-optimal-student-supervisor-allocation&metric=alert_status)](https://sonarcloud.io/dashboard?id=rithinch_pareto-optimal-student-supervisor-allocation)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

## Paper Publication

Applied Soft Computing Journal 2018.

[A near Pareto optimal approach to student–supervisor allocation with two sided preferences and workload balance.](https://arxiv.org/abs/1812.06474)

Distributed Computing and Artificial Intelligence, 15th International Conference. DCAI 2018.

[A Multi-objective Evolutionary Proposal for Matching Students to Supervisors.](https://link.springer.com/chapter/10.1007/978-3-319-94649-8_12)


## Problem Summary

The problem of allocating students to supervisors for the development of a personal project or a dissertation is a crucial activity in the higher education environment, as it enables students to get feedback on their work from an expert and improve their personal, academic, and professional abilities. In this project, we propose a multi-objective and near Pareto optimal genetic algorithm for the allocation of students to supervisors. The allocation takes into consideration the students and supervisors' preferences on research/project topics, the lower and upper supervision quotas of supervisors, as well as the workload balance amongst supervisors. We introduce novel mutation and crossover operators for the student-supervisor allocation problem. The experiments carried out show that the components of the genetic algorithm are more apt for the problem than classic components, and that the genetic algorithm is capable of producing allocations that are near Pareto optimal in a reasonable time.

## Authors
* Rithin Chalumuri (Pinewood Technologies, rithin.chalumuri@gmail.com)
* Dr. Victor Sanchez-Anguix (Universitat Politecnica de Valencia, vicsana1@upv.es)
* Dr. Reyhan Aydogan (Ozyegin University, reyhan.aydogan@ozyegin.edu.tr)
* Prof. Vicente Julian (Universitat Politècnica de València, vinglada@dsic.upv.es)

## Used by
* Florida Universitaria (Spain)
* London School of Economics (UK), Department of International Development

## Citation

If you found this useful for your research, please cite our work:

```
@article{sanchez2019near,
  title={A near Pareto optimal approach to student--supervisor allocation with two sided preferences and workload balance},
  author={Sanchez-Anguix, Victor and Chalumuri, Rithin and Aydo{\u{g}}an, Reyhan and Julian, Vicente},
  journal={Applied Soft Computing},
  volume={76},
  pages={1--15},
  year={2019},
  publisher={Elsevier}
}
```
