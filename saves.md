Information about additional edits which are possible in the JSON file
======================================================================

World game objects
------------------
  
In the file save (exportet as JSON) you have in `savedata->map->v->_wgos->v` a list with all "World Game Objects" of the game.  
Those include all interactable objects and more. The game saves the location of those. These include f.e. spots where hiccup grass grows, meaning you could change its location next to your house or even duplicate the objects (is what I assume, I didn't try it)  
Other interesting things you could change there are f.e. location of built objects, teleport spots (?, ids teleport_hatch, teleport_inside, teleport_outside, teleport_point - 1 teleport_hatch / teleport_inside / teleport_outside corresponds with 1 teleport_point because they have the same custom tag, meaning you probably can create new teleport points f.e. 1 infront of your house to the lighthouse) or NPC objects.  
Meaning if your NPC is broken you could try replacing it's data with the data from a save where it is not broken. (As far as I can tell no achievement or progress related data is stored in them, but I only took a look at a early game save).  
  
A list of a 10 Minute save with all the possible world game object ids and their amounts would be (as JSON):  

```JSON
{"swamp_table_constr":1,"swamp_bridge":1,"teleport_outside":13,"teleport_point":41,"mushroom_1":72,"fence_stone_h":14,"fence_wood_anc_b_1":20,"fence_wood_anc_r_2":3,"fence_wood_anc_f_1":16,"fence_wood_anc_b_0":5,"fence_wood_anc_b_10":4,"fence_wood_anc_f_0":2,"fence_wood_anc_r_10":2,"fence_wood_anc_r_4":1,"fence_wood_anc_r_1":6,"fence_wood_anc_r_0":1,"fence_wood_anc_l_10":3,"fence_wood_anc_l_2":2,"fence_wood_anc_l_1":6,"fence_wood_anc_f_10":3,"fence_wood_anc_f_6":6,"fence_wood_anc_f_4":4,"fence_wood_anc_b_5":2,"fence_wood_anc_b_4":3,"fence_wood_anc_b_2":3,"bat_test":10,"bonfire_burning":2,"mining_builddesk_broken":1,"d_obj_spiral_stair_stn_in_1":3,"teleport_inside":21,"teleport_hatch":5,"garden_builddesk_broken":1,"fence_wood_anc_l_0":5,"fence_wood_anc_l_4":5,"graveyard_zone_lvlup2":1,"graveyard_builddesk":1,"mf_wood_builddesk":1,"morgue_builddesk_broken":1,"church_builddesk":1,"cellar_builddesk":1,"tree_2_6":49,"tree_tiny_2":89,"tree_2_2":114,"tree_tiny_1":107,"tree_1_3":99,"bush_4":32,"bush_horizontal_3":42,"garden_grapes_broken":8,"flower_small_1":68,"flower_small_3":75,"flower_small_2":84,"flower_small_4":54,"flower_small_5":78,"flower_small_6":50,"flower_small_8":59,"flower_small_9":55,"roof_1":4,"beehouse_broken":4,"beegarden_table_broken":1,"tree_garden_builddesk":1,"stone_2":40,"tree_huge_1":10,"tree_old_2":23,"bush_5":219,"flower_small_7":83,"tree_old_1":24,"tree_old_3":21,"cremation_builddesk":1,"old_wood_stump_1":26,"old_wood_swamp_set_1":23,"old_wood_swamp_set_2":28,"wood_obstacle_steep_el":1,"wood_obstacle_v":1,"bush_horizontal_1":17,"bush_1_berry":7,"stone_4":30,"stone_3":19,"decor_stone":21,"stone_5":20,"stone_1":27,"land_clay_spot_1":2,"church_0":1,"npc_royal_box":1,"tree_mid_strip_1":17,"tree_3_1":43,"tree_mid_strip_2":17,"water_well":3,"mf_grindstone_1":2,"village_wc_Face":3,"house_1":1,"mf_box_stuff":4,"cooking_bonfire":2,"garden_of_stones_place":1,"witch_hut":1,"npc_witch":1,"church_closed_door":1,"morgue_1":1,"ruin_0":3,"morgue_throw_in_broken":1,"iron_ore":32,"stone_ore":3,"pile_of_sand":5,"lying_rock":1,"vegit_bracken_1":7,"vegit_bracken_2":43,"tree_2_1":35,"tree_2_4":73,"tree_3_4":23,"tree_3_3":34,"tree_1_2":76,"tree_2_5":50,"tree_3_2":39,"tree_tiny_3":83,"tree_1_1":55,"tree_1_4":54,"tree_3_3_stump":2,"tree_3_4_stump":3,"tree_1_1_stump":3,"bush_plump_2":36,"bush_2":100,"bush_horizontal_2":21,"bush_2_berry":10,"bush_3_berry":14,"mushroom_2":47,"hiccup_grass_3":4,"hiccup_grass_2":6,"hiccup_grass_1":8,"gate_wood_new_f_0":1,"fence_stone_v":5,"grave_ground":13,"lantern_obj":9,"tree_2_1_stump":8,"mf_timber_1":1,"mf_stones_1":1,"bridge_stn_broken":1,"tree_3_1_stump":4,"roof_2":3,"swamp_fishing_spot":1,"throw_body_river":1,"Tavern":1,"lantern_2":1,"mf_stones_1_decor":2,"mf_ore_1_complete_decor":6,"village_wc_Rgh":8,"stone_workshop_1":1,"village_house_1":2,"village_wc_Face_2":3,"village_house_2":1,"tree_3_4_bees_done":2,"tree_2_4_stump":2,"tree_2_5_stump":3,"tree_3_1_bees":1,"village_mill":1,"village_farmer_house_sml":1,"mole":3,"mill_broken_obj":1,"mf_anvil_2_decor":2,"mf_anvil_1_decor":1,"mf_anvil_3_decor":1,"mf_wood_panel_2_complete":1,"mf_coal_1_decor":2,"smithy_1":1,"barrel":14,"village_house_3":1,"garden_pumpkin_ready_village":4,"beehouse_decor":6,"garden_pumpkin":4,"tree_1_2_stump":1,"decor_tree_apple_1_flower":3,"tree_3_1_bees_done":3,"village_house_4":2,"npc_beekeeper":1,"garden_cabbage_ready_village":18,"village_house_5":1,"garden_carrot_ready_village":3,"garden_carrot":17,"garden_beet":14,"village_house_6":1,"garden_beet_ready_village":1,"garden_onion":11,"garden_grapes":3,"garden_lentils":9,"garden_cabbage_ready":2,"garden_cabbage":13,"village_house_7":1,"ruins_el_2":9,"garden_onion_ready_village":1,"garden_lentils_ready_village":1,"decor_tree_apple_2_green":2,"decor_tree_apple_3_red":1,"decor_tree_apple_1_red":4,"decor_tree_apple_2_flower":3,"camp_barrel_wagon":3,"village_farmer_house_mid":1,"village_henhouse":2,"village_hut_1":1,"egg_seller":1,"camp_horse_parking":1,"camp_tent_db_1":2,"camp_tent_df_1":1,"camp_tent_vf_1":2,"camp_tent_vf_2":1,"camp_wagon_chest_d":2,"camp_wagon_stuff":3,"camp_wagon_stuff_2":1,"campfire":2,"tree_1_4_stump":1,"storage_1":1,"decor_land_clay_spot_1":2,"mf_potter_wheel_1_decor":1,"npc_potter":1,"npc_shepherd":1,"npc_shepherds_wife":1,"farm":1,"sealman_house":1,"mf_timber_1_decor":2,"mf_beam_gantry_1_decor":2,"tree_2_2_stump":1,"garden_cannabis":11,"decor_mf_vine_press":1,"npc_dig":1,"village_pithos":1,"ruins_pillar_2":5,"burn_0":1,"tree_3_2_stump":1,"bonfire_smoldering":1,"npc_guard_9":1,"npc_guard_10":1,"forpost":1,"hatch_from_morgue":1,"mine":1,"sawmill_1":1,"big_broken_bridge":1,"lighthouse":1,"tree_1_3_stump":1,"ruins_viaduct_1":2,"ruins_viaduct_5":1,"ruins_viaduct_6":3,"ruins_viaduct_7":1,"ruins_viaduct_2":1,"ruins_pillar_1":7,"ruins_pillar_5":3,"ruins_pillar_6":3,"ruins_el_1":7,"turnpike_close":3,"nameplate_2":1,"npc_actor":1,"npc_gypsy":1,"npc_wood_cutter":1,"donkey":1,"npc_miller":1,"npc_blacksmith":1,"npc_farmer":1,"npc_tavern owner":1,"npc_captain":1,"npc_mrs chain":1,"npc_guard":1,"npc_guard_3":1,"npc_guard_4":1,"npc_guard_5":1,"npc_carpenter":1,"npc_engineer":1,"npc_farmers son":1,"talking_skull":1,"npc_redneck_1":1,"npc_redneck_2":1,"npc_redneck_3":1,"npc_redneck_4":1,"npc_redneck_5":1,"npc_redneck_6":1,"npc_guard_2":1,"npc_citizen_1":1,"npc_citizen_2":1,"npc_citizen_3":1,"npc_citizen_4":1,"npc_citizen_5":1,"npc_citizen_6":1,"npc_guard_torch":1,"npc_citizen_woman_1":1,"npc_citizen_woman_2":2,"npc_guard_6":1,"npc_guard_7":1,"npc_guard_8":1,"npc_alice":1,"npc_satyr":1,"npc_lilya":1,"npc_ghost":1,"npc_hunchback":1,"decor_tree_apple_2_red":4,"decor_tree_apple_3_green":4,"decor_tree_apple_1_green":6,"tree_apple_1_3_1":3,"tree_apple_1_3_3":2,"tree_apple_1_3_stump":3,"tree_apple_1_3_0":2,"fence_wood_anc_f_2":1,"garden_empty":1,"npc_light_keeper":1,"telescope":1,"tree_2_6_stump":1,"tree_3_3_squirrel":1,"village_lake_fishing_spot":1,"portal_marble":1,"marble_heap_mid_1":1,"marble_heap_mid_2":1,"marble_stand_inactive":1,"decor_tree_apple_3_flower":1,"steep_coal":2,"mf_stone_pile_1":1,"sea_fishing_spot":1,"witch_pylon":1,"mf_chocks_1_decor":1,"scarecrow":1,"river_fishing_spot":1,"idle_points_stock":3,"mining_hut":1,"steep_end_blue_L_obstruction":1,"steep_yellow_blockage":2,"steep_yellow_blockage_inactive":1,"steep_yellow_blockage_R_o":1,"tree_3_2_bees_done":2,"tree_3_3_bees_done":1,"tree_old_3_stump":1,"steep_marble":1,"steep_iron":1,"steep_stone":1,"mine_zombie":1,"barrel01_broken":5,"barrel03_broken":3,"tree_big_sawmill":1,"zombie_sawmill_unfinished_placer":1,"waterfall_fishing_spot":1,"bed":2,"cupboard":1,"oven":1,"hatch":2,"cooking_table":1,"cooking_stand":1,"chest":2,"stranger":1,"storage_builddesk":1,"box_pallet":1,"cashbox":1,"working_table":1,"empty":3,"dungeon_stairs":3,"barrel02_broken":6,"blockage_H_low":1,"mf_preparation_1":1,"mf_alchemy_survey":1,"church_candle":4,"bookcase_F_damaged":2,"bookcase_F_broken":2,"morgue_throw_out_broken":1,"d_obj_spiral_stair_stn_out_1":1,"flour_bag":3,"blockage_V_low":1,"dungeon_enter":1,"blockage_V_high":1,"blockage_H_high":2,"dungeon_obj_rack02":1,"dungeon_obj_vase02":3,"dungeon_obj_bench01_broken":1,"dungeon_grille_closed":2,"dungeon_grille_opened":2,"dungeon_obj_vase01_broken":3,"dungeon_obj_vase03":1,"dungeon_obj_vase01":1,"dungeon_obj_vase04":2,"dungeon_obj_table02":1,"dungeon_obj_chair_02_broken":1,"table_cultist_quest":1,"floor_grid_fire":1,"wall_cellar_1tile":1,"bookcase_F_broken_custom_zombie":1,"alchemy_builddesk":1,"sacrifice_builddesk":1,"zombie_in_mortuary":1,"church_pulpit":1,"church_bench":2,"church_altar":1,"donat_box_inside":1,"tavern_door03":2,"tavern_table":5,"bed_no_sleep_1":1,"obj_church_bookcase":1,"dungeon_obj_table05":1,"bed_no_sleep_2":1,"dungeon_obj_table01":1,"tavern_writers_table":1,"tavern_cupboard":1,"mining_hut_bed":1,"nameplate_1":1,"npc_bishop":1,"npc_actress":1,"npc_merchant":1,"npc_cultist":1,"npc_inquisitor":1,"npc_astrologer":1,"crafting_skull_3":1,"mf_chocks_1":1}
```

With this data (because all of them contain a location) it should be possible to recreate your current world map if you extract the base map (the underground) + the sprites of the id's.

You can also generate this list by yourself, if you export as JSON and then select the `.html` export. If you open that in the browser, the code to generate that list is shown in the console.

Achievements
------------

The number progress of achievements is stored in `savedata->achievements->v`
If you f.e. started to catch 200 fish, you could find the entry with "fish_200" in `_completed->v` and at the same index in `_completed_n->v` you can set it f.e. to 199 and then fish 1 more fish to get the achievement.  
Same is possible with other achievements.  

Workers
-------

References to your worker zombies are stored in `savedata->workers`. They are still saved within the wgo object.


They have inventories and sub inventories. F.e. they have an inventory which contains `portable_backpack` - this backpack can contain other items. (Which Porter Workers are currently transporting)


It is also possible to get information about the workers you have within a save. If you want to know for example what the efficiencies of your workers are, you can use the following code. (In the provided HTML export, because that contains the utility function used and the correct variables):

```JavaScript
// Iterate all the objects in the world
wgo.forEach((entry) => {   
    // Save the ID of our object to a name for easier access
    const name = entry.v.obj_id.v; 
    
    // If the ID is a worker zombie, we print out the object and the efficiency, and all used items of the worker
    if(name === "worker_zombie_1")
    {
        console.log(entry)
        // getValueForParamKey is one of the provided utility functions in a HTML exported save
        console.log(getValueForParamKey(entry.v["-1126421579"].v._params, "working_k"))
        // For every inventory item object, we map the object to the actual item ID
        console.log(entry.v["-1126421579"].v.inventory.v.map(item => item.v.id.v))
    }  
});
```

Unlocked Technologies
---------------------

In `savedata->unlocked_techs` are your unlocked technologies (obviously), but the editor doesn't feature anything there because you can simply give you red, green and blue points to get them.


___________________________________________________________

If someone else wants to extend this information about additional data in the save, feel free to do so.