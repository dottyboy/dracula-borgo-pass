shader_type spatial;
// Wall material for generated dungeons: everything above cut_height that stands between the camera and the player
// is discarded, so the character is never hidden behind a wall (the camera looks in from one side).
uniform sampler2D albedo_tex : source_color, filter_linear_mipmap, repeat_enable;
uniform vec4 albedo_col : source_color = vec4(1.0);
uniform sampler2D normal_tex : hint_normal, filter_linear_mipmap, repeat_enable;
uniform sampler2D tri_tex : source_color, filter_linear_mipmap, repeat_enable;
uniform vec4 tri_col : source_color = vec4(1.0);
uniform float tri_scale = 0.5;
uniform bool use_tri = false;
uniform bool use_albedo_tex = false;
uniform bool use_normal_tex = false;
uniform float roughness = 0.9;
uniform vec3 player_pos = vec3(100000.0, 0.0, 100000.0);
uniform vec3 cam_pos = vec3(0.0, 5.0, 5.0);
uniform float cut_radius = 3.2;
uniform float cut_height = 1.15;

varying vec3 wpos;
varying vec3 wnorm;

void vertex() {
	wpos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
	wnorm = normalize((MODEL_MATRIX * vec4(NORMAL, 0.0)).xyz);
}

void fragment() {
	vec2 to_cam = cam_pos.xz - player_pos.xz;
	float cl = max(length(to_cam), 0.001);
	vec2 dir = to_cam / cl;
	vec2 rel = wpos.xz - player_pos.xz;
	float ahead = dot(rel, dir);
	float lateral = abs(dot(rel, vec2(-dir.y, dir.x)));
	if (wpos.y > cut_height && ahead > -0.4 && ahead < min(cl, cut_radius * 1.8) && lateral < cut_radius) {
		discard;
	}
	vec4 a = albedo_col;
	if (use_albedo_tex) {
		a *= texture(albedo_tex, UV);
	}
	if (use_tri) {
		vec3 w = pow(abs(wnorm), vec3(4.0));
		w /= (w.x + w.y + w.z + 0.0001);
		vec4 t = texture(tri_tex, wpos.zy * tri_scale) * w.x + texture(tri_tex, wpos.xz * tri_scale) * w.y + texture(tri_tex, wpos.xy * tri_scale) * w.z;
		a = tri_col * t;
	}
	ALBEDO = a.rgb;
	ROUGHNESS = roughness;
	if (use_normal_tex) {
		NORMAL_MAP = texture(normal_tex, UV).xyz;
	}
}
