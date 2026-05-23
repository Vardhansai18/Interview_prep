what is system design:
 

what do you mean by scaling?

Real-World Example:

Consider running a bookstore. Initially, you might handle everything manually – tracking inventory, managing orders, and so on. However, as your business grows, this approach becomes impractical. You need a system to automate these tasks, ensuring that your business can scale efficiently. This is where system design comes in. 


System design interviews are a critical part of the hiring process for many tech roles. They assess your ability to:

Analyze requirements: Understand the problem and define the scope of the system.
Design components: Identify key components and their interactions.
Scale systems: Ensure the system can handle varying loads and data volumes.
Consider trade-offs: Balance factors like performance, cost, and complexity.


Scaling Concepts: Horizontal vs. Vertical Scaling
Let’s take a closer look at the two main types of scaling through the lens of both a physical bookstore and a web application.

Horizontal Scaling: Adding more machines or instances to handle increased load.
Vertical Scaling: Adding more resources (CPU, RAM, disk space) to an existing machine.
Example:

Imagine your bookstore initially runs out of a small shop. As the number of customers grows, you face two options to handle the increased load:

Vertical Scaling:
Move to a larger building.
This improves your capacity but has limits. There’s only so big a single building can get.
Horizontal Scaling:
Open new branches in different locations.
This approach offers better scalability and redundancy, as each branch can serve local customers and share the load.



![alt text](image.png)

if more customers comes to the book store , will shut down the store and build big shop 
![alt text](image-1.png) 


if more customers then : 
we are scaling vertically: 
![alt text](image-2.png)

what bigip companies do is open store in different locations 
![alt text](image-4.png)

Lets say in real life, if we want to build a basic application : 
![alt text](image-3.png)

Vertical Scaling:
Upgrade your server with more CPU, RAM, and disk space.
This can handle more users and requests, but there’s a limit to how much you can upgrade a single server.
Horizontal Scaling:
Deploy your application across multiple servers or data centers around the world.
This allows you to handle more traffic, provides redundancy, and reduces latency by serving users from the nearest location.



if have to deal with million of users then we need to scale 



costs do not scale linearly

![alt text](image-6.png)

4gb Ram:
![alt text](image-5.png) 

8gb Ram:
![alt text](image-7.png) 


Comparison Table:

Aspect	Bookstore Example	Web Application Example
Horizontal Scaling	Open multiple branches in various locations	Deploy app to multiple servers/data centers
Vertical Scaling	Expand to a bigger building	Increase CPU/RAM/Disk on a single server
Pros of Horizontal	Redundancy, scalable	Redundancy, scalable, reduced latency
Cons of Horizontal	Management complexity	Load balancing, synchronization
Pros of Vertical	Simpler to implement	Easier management
Cons of Vertical	Limited by physical space	Limited by hardware capacity






