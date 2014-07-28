Announcing Daybed 2.0
#####################

A while ago, we started a proof of concept for Daybed, a schema definition and
data validation service.

Since then, the goals and implementation of daybed changed quite a few times,
and I thought that would be interesting to outline what the changes were over
the time, and what's the current direction we're taking.

Daybed, first version
---------------------

The first version of daybed was pretty simple: you could define a model and
send data to the server that would validate against the definition you created
earlier.

This was working pretty great and we added atop of that a bunch of geographic
fields, so it was possible to valide different geometries.

Who can access what? First try.
-------------------------------

Then we decided it would make sense to have ACLs on top of the API. After
a bunch of time hacking, we came up with a solution for the ACLs that was
pretty cool to implement. Let me try to explain what we did:

Each model would be created with an ACL policy. This policy would tell who
can do what, for each type of data. The way we defined this was inspired by
how UNIX filesystems works. You would define a bunch of permissions, with
a binary mask and then we would use it to check if you had the right to do the
operation you would try.

Implementation wasn't really straightforward: we had to play with the concept
of groups (each user would be part of a group *for the current model*)
a concept of permissions, and the representation of the permissions was
different than what was stored.

Controlling who can do what is great, but we also needed a way to authenticate
our users.  The solution we started to look at was Mozilla Persona. While
I love mozilla persona, it turned out to not be what we wanted in our case, for
the following reasons:

- Persona is for browsers, and the target audience for Daybed is not only
  browsers. We want anyone with an access to the network to deal with daybed.
  So using Person wasn't a good fit here;
- 

And the second try
------------------

The current implementation tries to keep things focused on what matters: we
need a way to declare models and a way to define who can access to what.

To keep things simple, we ditched completely the concept of users for daybed,
in favor of tokens.

Each 

Being offline first
-------------------

- Already existing projects.
- How we try to be different from what exists.
- How do we deal with syncing.
