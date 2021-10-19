/*
 * Copyright 2015 MovingBlocks
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.terasology.tutorialWorldGeneration;
import org.slf4j.Logger;
import org.joml.Vector2f;
import org.joml.Vector2ic;
import org.terasology.engine.utilities.procedural.Noise;
import org.terasology.engine.utilities.procedural.SimplexNoise;
import org.terasology.engine.utilities.procedural.SubSampledNoise;
import org.terasology.engine.world.block.BlockAreac;
import org.terasology.engine.world.generation.Border3D;
import org.terasology.engine.world.generation.FacetProvider;
import org.terasology.engine.world.generation.GeneratingRegion;
import org.terasology.engine.world.generation.Produces;
import org.terasology.engine.world.generation.facets.ElevationFacet;
import org.slf4j.LoggerFactory;
import java.io.*;
import java.util.*;

class QuantumNoise extends SimplexNoise{
    private static final Logger logger = LoggerFactory.getLogger(QuantumNoise.class);

    QuantumNoise(long seed){
        super(seed);
    }
//    @Override
    static float noise123(float xin, float yin, float zin) {
        try {
            String command = "python ../../../../../../../../../../perlin.py " + xin + " " + yin + " " + zin;
            Process process = Runtime.getRuntime().exec(command);
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            float ret = 0.0f;
            while ((line = reader.readLine()) != null) {
                ret = Float.parseFloat(line);
                logger.trace(Float.toString(ret));
            }

            reader.close();
            return ret;
        } catch (Exception e) {
//            logger.trace(e.getMessge());
        }
        return 0.0f;
    }
    static float absolute(float z){
        return z > 0 ? z: -z;
    }
}

@Produces(ElevationFacet.class)
public class SurfaceProvider implements FacetProvider {

    private Noise surfaceNoise;

    @Override
    public void setSeed(long seed) {
        surfaceNoise = new SubSampledNoise(new SimplexNoise(seed), new Vector2f(0.01f, 0.01f), 1);
    }

    @Override
    public void process(GeneratingRegion region) {
        // Create our surface height facet (we will get into borders later)
        Border3D border = region.getBorderForFacet(ElevationFacet.class);
        ElevationFacet facet = new ElevationFacet(region.getRegion(), border);

        // loop through every position on our 2d array
        BlockAreac processRegion = facet.getWorldArea();
        for (Vector2ic position : processRegion) {
//            facet.setWorld(position, surfaceNoise.noise(position.x(), position.y()) * 20);
            facet.setWorld(position, QuantumNoise.noise123(QuantumNoise.absolute(position.x()%256), QuantumNoise.absolute(position.y()%256), 0));
        }

        // give our newly created and populated facet to the region
        region.setRegionFacet(ElevationFacet.class, facet);
    }
}
