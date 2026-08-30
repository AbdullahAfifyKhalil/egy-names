<?php

declare(strict_types=1);

use Afify\FakerEgyNames\Provider;
use Faker\Factory;
use Faker\Generator;

/**
 * Return a Faker instance with the Egyptian names provider already registered.
 */
function egyptian_faker(): Generator
{
    $faker = Factory::create();
    $faker->addProvider(new Provider($faker));

    return $faker;
}
