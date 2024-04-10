local wsp_op_script={}

-- register variants for variable
-- get data
function wsp_op_script.get_data_for_register(location, user_attribute)
    local data = {}
    local c = user_attribute:getNumberOfChildren()
    for i=0, c-1 do
        local i_atr = user_attribute:getChildByIndex(i)
        local i_atr_name = user_attribute:getChildName(i)
        if pystring.startswith(i_atr_name, 'data_') then
            local i_sample = i_atr:getSamples():get(0)
            local i_key = i_sample:get(0)
            local i_value = i_sample:get(1)
            if i_key ~= nil then
                data[i_key] = i_value
            end
        end
    end
    return data
end

-- register data
function wsp_op_script.register_by_data(data)
    for i_key, i_value in pairs(data) do
        Interface.SetAttr('lynxi.variants.'..i_key, StringAttribute(i_value))
    end
end

-- reverse face vertex indices
function reverse_fnc(start_indices, vertex_indices)
    local t = {}
    for i=2, #start_indices do
        local start_index = start_indices[i-1]+1
        local end_index = start_indices[i]
        for j=start_index, end_index do
            t[j] = vertex_indices[end_index-j+start_index]
        end
    end
    return t
end

function wsp_op_script.reverse_face_vertex_indices()
    local start_indices = Interface.GetAttr('geometry.poly.startIndex'):getNearestSample(1)
    local vertex_indices = Interface.GetAttr('geometry.poly.vertexList'):getNearestSample(1)

    Interface.SetAttr('geometry.poly.vertexList', IntAttribute(reverse_fnc(start_indices, vertex_indices)))
    Interface.SetAttr('viewer.default.drawOptions.windingOrder', StringAttribute('counterclockwise'))
    Interface.SetAttr('arnoldStatements.invert_normals', IntAttribute(0))

    local atr = Interface.GetAttr('geometry.arbitrary')
    local c = atr:getNumberOfChildren()
    for i=0, c-1 do
        local i_atr_name = atr:getChildName(i)
        local i_role_atr_path = 'geometry.arbitrary.' .. i_atr_name .. '.usd.role'
        local i_role_atr = Interface.GetAttr(i_role_atr_path)
        if i_role_atr ~= nil then
            if i_role_atr:getValue() == 'TextureCoordinate' then
                local i_vertex_indices = Interface.GetAttr('geometry.arbitrary.' .. i_atr_name .. '.index'):getNearestSample(1)
                Interface.SetAttr('geometry.arbitrary.' .. i_atr_name .. '.index',  IntAttribute(reverse_fnc(start_indices, i_vertex_indices)))
            end
        end
    end
end

function wsp_op_script.override_properties(atr_base, override_atr_name)
    local override_atr=Interface.GetOpArg(override_atr_name)
    local raw = override_atr:getValue()
    if (raw ~= nil) then
        local raw_ = pystring.split(raw, '\n')
        for i, i_s in ipairs(raw_) do
            if (i_s ~= '') then
                local i_s_ = pystring.split(i_s, '=')
                local i_name = pystring.rstrip(pystring.lstrip(i_s_[1]))
                local i_value = pystring.rstrip(pystring.lstrip(i_s_[2]))
                local i_atr_path = atr_base..'.'..i_name
                local i_atr = Interface.GetAttr(i_atr_path)
                if (i_atr == nil) then
                    if (i_value == '') then
                        Interface.SetAttr(i_atr_path, StringAttribute(i_value))
                    elseif (pystring.isdigit(i_value) == true) then
                        local i_value_ = tonumber(i_value)
                        if(pystring.find(i_value, '.') == -1) then
                            Interface.SetAttr(i_atr_path, IntAttribute(i_value_))
                        else
                            Interface.SetAttr(i_atr_path, FloatAttribute(i_value_))
                        end
                    else
                        Interface.SetAttr(i_atr_path, StringAttribute(i_value))
                    end
                else
                    if (Attribute.IsInt(i_atr)) then
                        local i_atr_value = tonumber(i_value)
                        Interface.SetAttr(i_atr_path, IntAttribute(i_atr_value))
                    elseif (Attribute.IsFloat(i_atr)) then
                        local i_atr_value = tonumber(i_value)
                        Interface.SetAttr(i_atr_path, FloatAttribute(i_atr_value))
                    elseif (Attribute.IsDouble(i_atr)) then
                        local i_atr_value = tonumber(i_value)
                        Interface.SetAttr(i_atr_path, DoubleAttribute(i_atr_value))
                    elseif (Attribute.IsString(i_atr)) then
                        local i_atr_value = tostring(i_value)
                        Interface.SetAttr(i_atr_path, StringAttribute(i_atr_value))
                    end
                end
            end
        end
    end
end


return wsp_op_script