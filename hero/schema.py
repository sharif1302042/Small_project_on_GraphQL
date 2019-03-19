import graphene
from graphene_django import DjangoObjectType
from .models import Author,Article


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        #fields = ('name', 'id')

class ArticleType(DjangoObjectType):
    class Meta:
        model = Article

##################################################
                        #query
##################################################
class Query(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)

    author=graphene.Field(AuthorType,
                          id=graphene.Int(),
                          name=graphene.String()
                          )


    all_articles=graphene.List(ArticleType)

    article = graphene.Field(
        ArticleType,
        id = graphene.Int(),
        category = graphene.String()
        )


    def resolve_all_authors(self, info, **kwargs):
        return Author.objects.all()

    def resolve_all_articles(self, info, **kwargs):
        return Article.objects.all()


    def resolve_author(self,info, **kwargs):
        #id = kwargs.get('id')
        name = kwargs.get('name')

        #if id is not None:
        #   return Author.objects.get(pk=id)

        if name is not None:
            return Author.objects.get(name=name)
        return None

    def resolve_article(self,info, **kwargs):
        id = kwargs.get('id')
        category = kwargs.get('category')

        if id is not None:
            return Article.objects.get(pk=id)

        if category is not None:
            return Article.objects.filter(category=category)[2]

            """
            a = list(Article.objects.filter(category=category))
            l=len(a)
            i=0
            for i in range(l):
                b=Article.objects.filter(category=category)[i]
                return b
            """
        return None

####################################################
                #mutations
####################################################
class AuthorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    phone_no = graphene.String()
    email = graphene.String()

class CreateAuthor(graphene.Mutation):
    class Arguments:
        input = AuthorInput(required= True)

    ok=graphene.Boolean()
    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info , input=None):
        ok= True
        author_instance=Author(name=input.name)
        author_instance.save()
        return CreateAuthor(ok=ok,author=author_instance)

class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input=AuthorInput(required=True)

    ok =graphene.Boolean()
    author=graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        author_instance = Author.objects.get(pk=id)
        if author_instance:
            ok =True
            author_instance.name=input.name
            #author_instance.phone_no=input.phone_no
            #author_instance.emain=input.email
            author_instance.save()
            return UpdateAuthor(ok=ok, author=author_instance)
        return UpdateAuthor(ok=ok, author=None)

class Mutation(graphene.ObjectType):
    create_author=CreateAuthor.Field()
    update_author=UpdateAuthor.Field()

###############################################
#for create
"""
mutation createActor {  
  createAuthor(input: {
    name: "ami",
    phoneNo: "01521250335",
    email: "sharif@gmail.com",
  }) {
    ok
    author {
      id
      name
      phoneNo
      email
    }
  }
}
"""
###############################################
#for update
"""
mutation
{
    updateAuthor(id: 2, input: {
    name: "vai",

}) {
    ok
author
{
    id
name

}
}
}
"""
##########################################


