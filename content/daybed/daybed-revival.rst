Daybed revival
##############

:date: 2014-07-29
:authors: Rémy Hubscher, Mathieu Leplatre, Alexis Métaireau

A while ago, we started a proof of concept for Daybed, a schema definition and
data validation service. We wanted to create such a system because we wanted
(into other things) to have a nice and open source alternative to google forms
(a tool provided by google to create forms).

Since then, the goals and implementation of daybed changed quite a few times,
and I thought that would be interesting to outline why we changed our mind and
what's the current direction we're taking.

Proof of concept
----------------

The first version of daybed was pretty simple: you could define a model and
send data to the server that would validate against the definition you created.

This was working pretty great and we added atop of that a bunch of geographic
fields, so it was possible to valide different geometries.

The scope is still quite similar to this, but we found that the set of features
this provides wasn't enough for our use cases.

Adding Access control to the mix
--------------------------------

Then we decided it would make sense to have ACLs on top of the API. After
a bunch of time hacking, we came up with a working solution.

Each model would be created with an ACL policy attached to it. This policy
would tell who can do what, for each kind of data attached to a model (the
definition, the data, and the ACLs).

The way we defined this was inspired by how UNIX filesystems works. You would
define a bunch of permissions, with a binary mask and then we would use it to
check if you had the right to do the operation you would try.

Implementation wasn't really straightforward, though. We had to play with the
concept of groups (each user would be part of a group *for the current model*)
a concept of permissions, and an abstraction on top of that (called policies)
so that users wouldn't need to define each time the policy for a model.

This had a number of drawbacks: dealing with ACLs was painful and you had to
think about the users for an instance of daybed, groups for the users and so
on.

Don't get me wrong, users, groups and policies are pretty useful and valid
concepts, but exposing them to the consumer of the API just happened to make
the API more complex to use.


Getting it right
----------------

We had other duties for a time and when we got back to Daybed, we were a bit
affraid of the monster we created. "What's wrong with this API? It used to be
simple!"

We sat back and gave some thoughts to all this. How can we deal with ACLs in
a simple and straightforward way?

The current implementation tries to keep things focused on what matters: we
need a way to declare models and a way to define who can access to what.
Period.

To keep things simple, we ditched completely the concept of users, groups and
policies, in favor of tokens.

This has the side-effect of keeping things really simple to think, and simple
to implement.

Let's have a look at the steps required to use daybed:

1. Generate or register a keypair with a `POST` or `PUT` on `/tokens`;
2. Define a model by doing a `POST` or a `PUT` on `/model` (Alternately, you can
   just reuse one existing model);
3. Post data to this model using `POST` on `/model/{name}/data`;
4. Retrieve data back using `GET` on `/model/{name}/data`.

(Steps 2, 3 and 4 can be authenticated if you want to deal with ACLs).

And that's it. You don't need to think about anything else, that just works.
In case the data you sent is not valid, you would get some feedback from the
server telling you why it's not valid, and otherwise it will just be stored.

Authentication, revisited
-------------------------

Controlling who can do what is great, but we also needed a way to authenticate
our users.  The solution we started to look at was Mozilla Persona. While
I love mozilla persona, it turned out to not be what we wanted in our case, for
the following reasons:

- Persona is for browsers, and the target audience for Daybed is not only
  browsers. We want anyone with an access to the network to deal with daybed.
  So using Person wasn't a good fit here;
- We had trouble making it work like we wanted, because the concepts behind
  persona are quite complex. And that something we wanted to avoid to our end
  users.

We finally decided to implement the hawk authentication scheme. If you're not
familiar with this, it can be seen as the successor of OAuth, but a lot
simpler to use.

To authenticate to daybed, you then just need to send your Hawk credentials
(using an hawk-compatible client), and whoever registers to daybed can get some
in a glimpse.

What's next?
------------

These are the choices we made for Daybed, and we're currently finishing the
implementation of all that (it should be out really soon). 

We still have a lot on our plate, but the direction we're going seem pretty
straightforward for now:

- We need to implement a javascript library that consumes the Daybed APIs.
  We're not sure yet of the form it will take, but reading a lot of
  documentation and code for other projects makes me think we want to go for an
  event-driven, object oriented thing;
- We're working on an app that will benefit from Daybed at Mozilla (Rémy and I
  are working there), so it helps us to stay focused;
- Being offline first. That makes a lot of sense to use daybed in a no-backend
  environment, even if that sounds a bit weird, and that's something we're
  experimenting with. This means we're dealing with Syncing and the javascript
  API should work without the need of a daybed server.

We're very excited about all this, so keep posted, news to come!
