import pygame
pygame.init()
width, height = 1536, 864
screen = pygame.display.set_mode((width, height))

tb_border_width = 90
tb_border_color = (0, 0, 0)
hearts_color = (255, 255, 255)

amount_required_for_new_level = 3


player_health = 5

initial_proj_speed = 1
max_proj_speed = 4
linear_increment_proj_speed = .8
level_square_width = 90

heart_slowdown = 5

amount_proj_trail = 20

col_text_boxes = (155, 155, 155)


class Topics:
    def __init__(self) -> None:
        self.default_color = pygame.math.Vector3(200, 200, 200)

        self.environment_color = pygame.math.Vector3(0, 250, 0)
        self.environment_current_time = 0
        self.environment_current_color = pygame.math.Vector3(155, 155, 155)

        self.history_color = pygame.math.Vector3(165, 42, 42)
        self.history_current_time = 0
        self.history_current_color = pygame.math.Vector3(155, 155, 155)

        self.math_color = pygame.math.Vector3(50, 50, 50)
        self.math_current_time = 0
        self.math_current_color = pygame.math.Vector3(155, 155, 155)

        self.science_color = pygame.math.Vector3(250, 150, 160)
        self.science_current_time = 0
        self.science_current_color = pygame.math.Vector3(155, 155, 155)

        self.custom_color = pygame.math.Vector3(255, 255, 255)
        self.custom_current_time = 0
        self.custom_current_color = pygame.math.Vector3(155, 155, 155)


qa = [

    [
        ("CA's primary source of energy is natural ___", 'gas'),
        ('What is the main cause of air pollution in CA?', 'transportation'),
        ('CA addressing the issue of water scarcity with water ___?', 'efficiency'),
        ("CA's primary source of renewable energy is solar __?", 'power'),
        ('Largest source of greenhouse gas emissions in CA?', 'transportation'),
        ('What is the main type of vegetation found in CA?', 'mediterranean'),
        ('What is the main cause of deforestation in CA?', 'urbanization'),
        ('What is the main type of habitat found in CA?', 'forests'),
    ],



    [
        ('When did World War II end?', '1945'),
        ('Who was the first president of the United States?', 'washington'),
        ('Ship that carried the Pilgrims to the New World?', 'mayflower'),
        ('Leader of the Soviet Union during World War II?',
         'stalin'),
        ('Who was the leader of Germany during World War II?', 'hitler'),
        ('Policy of segregation in the United States is jim ___', 'crow'),
        ('Who invented the steam engine?', 'watt')
    ],





    [
        ('Integer closest to PI?', '3'),
        ('What is the square root of 4?', '2'),
        ('Slope of line with equation y=5x+4', '5'),
        ('Area of triangle with length 3 and height 6?', '9'),
        ('Circumference of circle with radius 6/pi?', '12'),
        ('Volume of cube with length 3?', '27'),
        ('Is shoelace formula the best mathematical formula?', 'yes'),
        ('Volume of sphere with radius 3 divided by pi', '36'),
        ('Surface area of rectangular prism with lengths: 3, 4, 5',
         '78'),
        ('Perimeter of square with length 1', '4')
    ],





    [
        ('What atom does water have two of?', 'hydrogen'),
        ('Process by which plants make their own food?', 'photosynthesis'),
        ('What is the fundamental unit of life?', 'cell'),
        ('Force that causes objects to fall to the ground?', 'gravity'),
        ('What is the scientific study of the earth?', 'geology'),
        ('What is the study of the universe?', 'astronomy'),
        ('What is the study of matter and energy?', 'physics'),
        ('What is the study of living organisms?', 'biology'),
        ('What is the outer layer of the Earth?', 'crust')
    ],

    []
]


environment = 0
history = 1
math = 2
science = 3
custom = 4
