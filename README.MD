# AirBnB Clone Project
> A custom version of AirBnB

## Welcome to the HBNB project

This project is part of my curriculum at Holberton School. It is the third major group project, marking a new milestone in our journey as full-stack developers. Developed in close collaboration with two other students, its purpose is to design and build a complete web application that replicates the core functionalities of the AirBnB platform.

The project aims to provide users with an intuitive and secure interface to publish, search, and book accommodations. It is built following a layered architecture, combining front-end and back-end components, and adheres to rigorous technical and stylistic standards. This README details the requirements, structure, and implementation strategies that guided the development of our own AirBnB clone — codenamed HBNB.

## Navigation

- [HBnB - UML](#hbnb---uml)
- [HBnB - BL and API](#hbnb---bl-and-api)
- [HBnB - Auth & DB](#hbnb---auth-and-db)
- [HBnB - Simple Web Client](#hbnb---simple-web-client)

---

# HBnB - UML

As a preliminary step before implementation, this subproject focuses on designing the core architecture of the HBnB application using UML (Unified Modeling Language). The objective is to plan, model, and document the main components of the system — including users, places, reviews, and amenities — through a set of standardized diagrams.

- The goal is to produce clear, structured documentation that will guide the development of the full application. This includes:
- A high-level package diagram to illustrate modular organization.
- A detailed class diagram representing the business logic layer.
- Sequence diagrams that map out key user interactions via the API.
- A final compilation of all these elements into a cohesive technical blueprint.

This modeling phase ensures consistency, modularity, and clarity before the actual coding begins, laying a strong foundation for the HBnB project.

[UML](https://github.com/Aluranae/holbertonschool-hbnb/tree/main/part1)

<p align="right"><a href="#navigation">↑ Back to Navigation</a></p>

---

# HBnB - BL and API

This subproject marks the beginning of the actual implementation of the HBnB application. Building on the UML design phase, it focuses on coding the **Business Logic** and **API** layers using **Python**, **Flask**, and **flask-restx**.

## Objective

The goal is to bring the previously documented architecture to life by:

- Structuring the project into clean, modular packages.
- Defining the core business entities (`User`, `Place`, `Review`, `Amenity`) and their relationships.
- Implementing the **facade pattern** to coordinate logic across services.
- Developing **RESTful API endpoints** to support full CRUD operations.
- Returning enriched serialized data (e.g., owner info, related amenities).
- Testing and validating all endpoints manually via Postman or cURL.

⚠️ Authentication, role management, and persistence in a real database will be introduced in later phases. For now, this project establishes a solid, testable API and a robust logic layer — setting the stage for full application deployment.

[BL and API](https://github.com/Aluranae/holbertonschool-hbnb/tree/main/part2)

<p align="right"><a href="#navigation">↑ Back to Navigation</a></p>

---

# HBnB - Auth and DB



[Auth & DB](https://github.com/Aluranae/holbertonschool-hbnb/tree/main/part3)

<p align="right"><a href="#navigation">↑ Back to Navigation</a></p>

---

# HBnB - Simple Web Client



[Simple Web Client](https://github.com/Aluranae/holbertonschool-hbnb/tree/main/part4)

<p align="right"><a href="#navigation">↑ Back to Navigation</a></p>

---

## Authors
<p align="right"><a href="#navigation">↑ Back to Navigation</a></p>

[Benjamin Estrada](https://github.com/Aluranae)  
[Mylliah](https://github.com/Mylliah)  
[ninaglss](https://github.com/ninaglss15)