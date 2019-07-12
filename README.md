# customAnime

## this one is based on [ktaebum](https://github.com/ktaebum)'s job,you can view it from [here](https://github.com/ktaebum/AttentionedDeepPaint)

this one is a temp project that provide a trained model of deepunet for painting the sketch.

in this web model you can just download the model from [here](https://drive.google.com/open?id=1J9o8uFBAkTpagBOLJc5jApFFWg-gyWLz)

## how to use?

1. download the model and put it into checkpoint folder
2. python manage.py runserver 0.0.0.0:8000
3. open 127.0.0.1:8000 in your explorer(I think all explorer is okay)
4. choose four color and upload a sketch(you can find some sketch by google sketch,there are also some test files in ./media)
5. now you get the painted one



## problems exist
1. 4 color is not enough,in fact,this program can get 20 color.but I don't have enough time design the front page.
2. even you provide 4 color,some part of the sketch didn't follow these four color.we have to assume this is because the model
3. not beautiful at all,like i said, this is just a temp project.
